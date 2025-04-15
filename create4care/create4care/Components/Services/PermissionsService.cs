using System.Threading.Tasks;
using Microsoft.Maui.ApplicationModel;

namespace create4care.Components.Services;

public class PermissionsService
{
    public async Task<bool> RequestCameraPermissionAsync()
    {
        var status = await Permissions.CheckStatusAsync<Permissions.Camera>();
        if (status != PermissionStatus.Granted)
        {
            status = await Permissions.RequestAsync<Permissions.Camera>();
        }
        return status == PermissionStatus.Granted;
    }
}
