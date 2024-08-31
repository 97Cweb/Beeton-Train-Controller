import asyncio
import logging
from zigbee_gateway.config_loader import load_config
from zigbee_gateway.gateway_manager import GatewayManager

async def main():
    config = load_config('config.yaml')
    gateway = GatewayManager(config)
    await gateway.create()

    # Example commands
    await gateway.permit_join(enable=True, duration=60)  # Enable joining
    await gateway.permit_join(enable=False)  # Disable joining
    gateway.list_devices()  # List all devices
    await gateway.remove_device('00:0d:6f:ff:fe:bc:4a:ef')  # Remove a specific device

    # Keep the script running to manage devices
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
