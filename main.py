"""
This file checks for changes in public IP address and updates a CloudFlare A or
AAAA record in the event of a change.
"""

if __name__ == "__main__":
    import shelve
    import _gdbm
    from os.path import dirname, realpath
    from os import remove
    from cf_ddns.ipcheck import IPCheck
    from pycf.cloudflare import DNSRecords
    import yaml

    config_file = dirname(realpath(__file__)) + "/config.yml"
    saved_config = open(config_file)
    cf_config = yaml.safe_load(saved_config)["cloudflare"]
    saved_config.close()

    ipc = IPCheck()
    cf = DNSRecords(cf_config["email"], cf_config["api_key"])

    addr_file = dirname(realpath(__file__)) + "/data/addrs"
    try:
        addrs = shelve.open(addr_file)

        current_v4 = ipc.v4_check()
        current_v6 = ipc.v6_check()

        try:
            if addrs["4"] == current_v4:
                pass
            elif addrs["4"] != current_v4:
                cf.update_record(
                    cf_config["zone_id"],
                    cf_config["v4_record_id"],
                    id=cf_config["v4_record_id"],
                    type="A",
                    content=current_v4,
                    name=cf_config["record_name"],
                )
                addrs["4"] = current_v4
        except KeyError:
            addrs["4"] = current_v4
        try:
            if addrs["6"] == current_v6:
                pass
            elif addrs["6"] != current_v6:
                cf.update_record(
                    cf_config["zone_id"],
                    cf_config["v6_record_id"],
                    id=cf_config["v6_record_id"],
                    type="AAAA",
                    content=current_v6,
                    name=cf_config["record_name"],
                )
                addrs["6"] = current_v6
        except KeyError:
            addrs["6"] = current_v6
        addrs.close()
    except _gdbm.error:
        remove(addr_file)
        raise Exception("Deleted corrupt address file")
