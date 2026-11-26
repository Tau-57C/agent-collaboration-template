using System;
using System.Diagnostics;
using System.IO;
using System.IO.Compression;
using System.Reflection;
using System.Text;
using System.Text.RegularExpressions;
using System.Windows.Forms;

internal static class Installer
{
    private const string Title = "Agent Collaboration Setup";

    [STAThread]
    private static int Main(string[] args)
    {
        if (args.Length == 2 && (args[0] == "--preview" || args[0] == "--install"))
            return RunFromCommandLine(args[1], args[0] == "--preview");
        if (args.Length != 0)
            return 2;

        Application.EnableVisualStyles();
        Application.SetCompatibleTextRenderingDefault(false);
        using (var picker = new FolderBrowserDialog())
        {
            picker.Description = "Choose the root folder of a new or existing project.";
            picker.ShowNewFolderButton = true;
            picker.SelectedPath = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
            if (picker.ShowDialog() != DialogResult.OK)
                return 0;

            try
            {
                Install(picker.SelectedPath, false);
                var message = "Installed in: " + picker.SelectedPath
                    + "\n\nOpen this project in your assistant."
                    + "\nNew project: Initialize collaboration."
                    + "\nExisting project: Import the existing project.";
                MessageBox.Show(message, Title, MessageBoxButtons.OK, MessageBoxIcon.Information);
                return 0;
            }
            catch (Exception error)
            {
                MessageBox.Show(error.Message, Title, MessageBoxButtons.OK, MessageBoxIcon.Error);
                return 1;
            }
        }
    }

    private static int RunFromCommandLine(string target, bool preview)
    {
        try
        {
            var result = Install(target, preview);
            using (var output = new StreamWriter(Console.OpenStandardOutput(), new UTF8Encoding(false)))
                output.WriteLine(result);
            return 0;
        }
        catch (Exception error)
        {
            using (var output = new StreamWriter(Console.OpenStandardError(), new UTF8Encoding(false)))
                output.WriteLine(error.Message);
            return 1;
        }
    }

    private static string Install(string target, bool preview)
    {
        target = Path.GetFullPath(target);
        if (!Directory.Exists(target))
            throw new DirectoryNotFoundException("Choose an existing folder for the project.");

        var python = FindPython();
        var parent = new DirectoryInfo(Path.GetTempPath()).FullName.TrimEnd(Path.DirectorySeparatorChar);
        var work = Path.Combine(parent, "agent-template-install-" + Guid.NewGuid().ToString("N"));
        if (!String.Equals(Path.GetDirectoryName(Path.GetFullPath(work)), parent,
                           StringComparison.OrdinalIgnoreCase))
            throw new IOException("Could not create the temporary setup directory.");

        Directory.CreateDirectory(work);
        try
        {
            string archive = Path.Combine(work, "template.zip");
            using (var resource = Assembly.GetExecutingAssembly().GetManifestResourceStream("TemplateData"))
            using (var destination = File.Create(archive))
            {
                if (resource == null)
                    throw new InvalidDataException("Setup is missing the template payload.");
                resource.CopyTo(destination);
            }
            ZipFile.ExtractToDirectory(archive, work);

            string option = preview ? "--dry-run" : "--apply";
            var result = python.Run("tools\\install.py " + Quote(target) + " " + option, work);
            if (result.ExitCode != 0)
                throw new InvalidOperationException(String.IsNullOrWhiteSpace(result.Errors)
                    ? "The file installer could not finish." : result.Errors.Trim());
            return result.Output.Trim();
        }
        finally
        {
            try { Directory.Delete(work, true); }
            catch (IOException) { }
            catch (UnauthorizedAccessException) { }
        }
    }

    private static PythonCommand FindPython()
    {
        var candidates = new[]
        {
            new PythonCommand(Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Windows), "py.exe"), "-3 "),
            new PythonCommand("python.exe", "")
        };
        foreach (var candidate in candidates)
        {
            try
            {
                var result = candidate.Run(
                    "-c \"import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)\"",
                    Environment.SystemDirectory);
                if (result.ExitCode == 0)
                    return candidate;
            }
            catch (System.ComponentModel.Win32Exception) { }
        }
        throw new InvalidOperationException("Setup requires Python 3.11 or later. Make it available through py -3 or python, then try again.");
    }

    private static string Quote(string text)
    {
        return "\"" + Regex.Replace(text, @"(\\*)(""|$)",
            match => match.Groups[1].Value + match.Groups[1].Value
                + (match.Groups[2].Value.Length == 0 ? "" : "\\\"")) + "\"";
    }

    private sealed class PythonCommand
    {
        private readonly string executable;
        private readonly string prefix;

        internal PythonCommand(string executable, string prefix)
        {
            this.executable = executable;
            this.prefix = prefix;
        }

        internal ProcessResult Run(string arguments, string folder)
        {
            var start = new ProcessStartInfo(executable, prefix + arguments);
            start.WorkingDirectory = folder;
            start.UseShellExecute = false;
            start.CreateNoWindow = true;
            start.RedirectStandardOutput = true;
            start.RedirectStandardError = true;
            start.StandardOutputEncoding = Encoding.UTF8;
            start.StandardErrorEncoding = Encoding.UTF8;
            start.EnvironmentVariables["PYTHONUTF8"] = "1";
            start.EnvironmentVariables["PYTHONIOENCODING"] = "utf-8";

            using (var process = Process.Start(start))
            {
                var stdout = process.StandardOutput.ReadToEndAsync();
                var stderr = process.StandardError.ReadToEndAsync();
                process.WaitForExit();
                return new ProcessResult(process.ExitCode, stdout.Result, stderr.Result);
            }
        }
    }

    private sealed class ProcessResult
    {
        internal readonly int ExitCode;
        internal readonly string Output;
        internal readonly string Errors;

        internal ProcessResult(int code, string output, string errors)
        {
            ExitCode = code;
            Output = output;
            Errors = errors;
        }
    }
}
