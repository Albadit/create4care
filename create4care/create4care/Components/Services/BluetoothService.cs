using Plugin.BLE;
using Plugin.BLE.Abstractions.Contracts;
using Plugin.BLE.Abstractions.EventArgs;
using System;
using System.Text;
using System.Threading.Tasks;

namespace create4care.Components.Services;

public class BluetoothService
{
    IAdapter _adapter;
    IBluetoothLE _ble;
    IDevice _device;
    IService _service;
    ICharacteristic _characteristic;

    // Convert 16-bit UUIDs to full 128-bit format.
    Guid serviceUuid = Guid.Parse("0000180C-0000-1000-8000-00805F9B34FB");
    Guid characteristicUuid = Guid.Parse("00002A56-0000-1000-8000-00805F9B34FB");

    // Events to notify the UI
    public event Action<string> OnStatusChanged;
    public event Action<string> OnDataReceived;

    public BluetoothService()
    {
        _ble = CrossBluetoothLE.Current;
        _adapter = CrossBluetoothLE.Current.Adapter;
    }

    public async Task ConnectAsync()
    {
        OnStatusChanged?.Invoke("Scanning for devices...");
        try
        {
            _adapter.DeviceDiscovered += (s, a) =>
            {
                if (!string.IsNullOrEmpty(a.Device.Name) &&
                    a.Device.Name.Equals("Arduino_R4_WiFi", StringComparison.Ordinal))
                {
                    _device = a.Device;
                }
            };

            await _adapter.StartScanningForDevicesAsync();

            if (_device == null)
            {
                OnStatusChanged?.Invoke("Device not found.");
                return;
            }

            OnStatusChanged?.Invoke($"Connecting to {_device.Name}...");
            await _adapter.ConnectToDeviceAsync(_device);

            int mtu = await _device.RequestMtuAsync(50);
            System.Diagnostics.Debug.WriteLine($"MTU requested: {mtu}");

            _service = await _device.GetServiceAsync(serviceUuid);
            if (_service == null)
            {
                OnStatusChanged?.Invoke("Service not found.");
                return;
            }

            _characteristic = await _service.GetCharacteristicAsync(characteristicUuid);
            if (_characteristic == null)
            {
                OnStatusChanged?.Invoke("Characteristic not found.");
                return;
            }

            if (_characteristic.CanUpdate)
            {
                _characteristic.ValueUpdated += Characteristic_ValueUpdated;
                await _characteristic.StartUpdatesAsync();
                OnStatusChanged?.Invoke("Connected. Waiting for data...");
            }
            else
            {
                OnStatusChanged?.Invoke("Characteristic doesn't support notifications.");
            }
        }
        catch (Exception ex)
        {
            OnStatusChanged?.Invoke($"Error: {ex.Message}");
        }
    }

    private void Characteristic_ValueUpdated(object sender, CharacteristicUpdatedEventArgs e)
    {
        // Convert the incoming byte array (JSON data) to a string.
        string json = Encoding.UTF8.GetString(e.Characteristic.Value);
        OnDataReceived?.Invoke(json);
    }
}
