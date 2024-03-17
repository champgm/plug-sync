from configuration import get_config, Config
from kasa import SmartPlug
import asyncio


async def main(config: Config):
    for plug_set in config.plug_sets:
        print("--------------------")
        print(f"Primary IP: {plug_set.primary_ip}")
        primary = SmartPlug(plug_set.primary_ip)
        try:
            await primary.update()
            turn_to = "on" if primary.is_on else "off"
            print(f"  {plug_set.primary_ip} plug is {turn_to}")
        except Exception as e:
            print(f"  Failed to connect to {plug_set.primary_ip}: {e}")
            continue
        print(f"  There are {len(plug_set.mirror_ips)} mirror plugs")
        for mirror_ip in plug_set.mirror_ips:
            print(f"    Mirror IP: {mirror_ip}")
            mirror = SmartPlug(mirror_ip)
            try:
                await mirror.update()
                if mirror.is_on:
                    print(f"      {mirror_ip} plug is on")
                else:
                    print(f"      {mirror_ip} plug is off")
            except Exception as e:
                print(f"      Failed to connect to {mirror_ip}: {e}")
                continue
            if primary.is_on != mirror.is_on:
                print(f"      Turning {mirror_ip} plug {turn_to}")
                if primary.is_on:
                    await mirror.turn_on()
                else:
                    await mirror.turn_off()
            else:
                print(f"      {mirror_ip} plug is already {turn_to}")
            print("      Done.")


async def loop_with_delay(config: Config):
    while True:
        await main(config)
        print(f"Will wait {config.check_interval}s before checking again")
        await asyncio.sleep(config.check_interval)


if __name__ == "__main__":
    config: Config = get_config()
    asyncio.run(loop_with_delay(config))
