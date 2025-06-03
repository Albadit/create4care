using Android;
using Android.App;
using Android.Content.PM;
using Android.OS;
using System.Runtime.Versioning;

namespace create4care;

[Activity(Theme = "@style/Maui.SplashTheme", MainLauncher = true, ConfigurationChanges = ConfigChanges.ScreenSize | ConfigChanges.Orientation | ConfigChanges.UiMode | ConfigChanges.ScreenLayout | ConfigChanges.SmallestScreenSize | ConfigChanges.Density)]
[SupportedOSPlatform("android31.0")] 
public class MainActivity : MauiAppCompatActivity
{
    protected override void OnCreate(Bundle? savedInstanceState)
    {
        base.OnCreate(savedInstanceState);

        if (Build.VERSION.SdkInt >= BuildVersionCodes.S)
        {
            if (CheckSelfPermission(Manifest.Permission.Camera) != Permission.Granted ||
                CheckSelfPermission(Manifest.Permission.BluetoothScan) != Permission.Granted ||
                CheckSelfPermission(Manifest.Permission.BluetoothConnect) != Permission.Granted
                )
            {
                RequestPermissions(
                [
                    Manifest.Permission.Camera,
                    Manifest.Permission.BluetoothScan,
                    Manifest.Permission.BluetoothConnect,
                ], 0);
            }
        }
    }
}
