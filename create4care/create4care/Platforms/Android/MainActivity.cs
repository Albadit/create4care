using Android;
using Android.App;
using Android.Content.PM;
using Android.OS;
// using Android.Webkit;

namespace create4care;

[Activity(Theme = "@style/Maui.SplashTheme", MainLauncher = true, ConfigurationChanges = ConfigChanges.ScreenSize | ConfigChanges.Orientation | ConfigChanges.UiMode | ConfigChanges.ScreenLayout | ConfigChanges.SmallestScreenSize | ConfigChanges.Density)]
public class MainActivity : MauiAppCompatActivity
{
    protected override void OnCreate(Bundle? savedInstanceState)
    {
        base.OnCreate(savedInstanceState);

        // Vraag runtime-permissies aan voor Android 12 (API level 31) en hoger.
        if (Build.VERSION.SdkInt >= BuildVersionCodes.S)
        {
            if (CheckSelfPermission(Manifest.Permission.Camera) != Permission.Granted ||
                CheckSelfPermission(Manifest.Permission.BluetoothScan) != Permission.Granted ||
                CheckSelfPermission(Manifest.Permission.BluetoothConnect) != Permission.Granted ||
                CheckSelfPermission(Manifest.Permission.BluetoothAdvertise) != Permission.Granted)
            {
                RequestPermissions(new string[]
                {
                    Manifest.Permission.Camera,
                    Manifest.Permission.BluetoothScan,
                    Manifest.Permission.BluetoothConnect,
                    Manifest.Permission.BluetoothAdvertise
                }, 0);
            }
        }
    }
}
