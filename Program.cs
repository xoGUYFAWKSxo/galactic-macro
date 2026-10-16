namespace GalacticMacro;

internal static class Program
{
    /// <summary>The app icon at every embedded size, for window title bars and the taskbar.</summary>
    public static readonly Icon AppIcon = new(typeof(Program).Assembly.GetManifestResourceStream("GalacticMacro.icon.ico")!);

    [STAThread]
    private static void Main()
    {
        ApplicationConfiguration.Initialize();
        Application.Run(new MainForm());
    }
}
