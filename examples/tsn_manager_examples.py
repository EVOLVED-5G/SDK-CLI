import random

from evolved5g.sdk import TSNManager


tsn_https_host = "localhost"
tsn_https_port = 5000
netapp_name_ids = {}
netapp_ids_tokens = {}
netapp_name = "MyNetapp"
tsn = TSNManager(
    https=False, tsn_https_host=tsn_https_host, tsn_https_port=tsn_https_port
)


def showcase_get_tsn_profiles():

    profiles = tsn.get_tsn_profiles()
    for profile in profiles:
        profile_configuration = profile.get_configuration_for_tsn_profile()
        profile_configuration_parameters = (
            profile_configuration.get_profile_configuration_parameters()
        )
        print(
            f"Profile {profile.name} with configuration parameters {profile_configuration_parameters}"
        )


def showcase_apply_tsn_profile_to_netapp():

    profiles = tsn.get_tsn_profiles()
    random.seed(1131)
    profile_to_apply = random.choice(profiles)
    profile_configuration = profile_to_apply.get_configuration_for_tsn_profile()

    netapp_identifier = tsn.NetappTrafficIdentifier(netapp_name=netapp_name)
    netapp_name_ids[netapp_name] = netapp_identifier

    print(f"Generated TSN traffic identifier for Netapp: {netapp_identifier.value()}")
    print(
        f"Apply {profile_to_apply.name} with configuration parameters"
        f"{profile_configuration.get_profile_configuration_parameters()} to NetApp {netapp_name} "
    )
    clearance_token = tsn.apply_tsn_profile_to_netapp(
        profile=profile_to_apply, netapp_traffic_identifier=netapp_identifier
    )
    print(
        f"The profile configuration has been applied to the netapp. The returned token {clearance_token} can be used "
        f"to reset the configuration"
    )
    netapp_ids_tokens[netapp_identifier.value()] = clearance_token


def showcase_clear_profile_configuration_from_netapp(netapp_name=netapp_name):
    netapp_identifier = netapp_name_ids[netapp_name]
    netapp_clearance_token = netapp_ids_tokens[netapp_identifier.value()]
    tsn.clear_profile_for_traffic_identifier(
        netapp_traffic_identifier=netapp_identifier,
        clearance_token=netapp_clearance_token,
    )


def showcase_apply_tsn_profile_with_overriden_parameters():

    profiles = tsn.get_tsn_profiles()
    random.seed(1131)
    profile_to_apply = random.choice(profiles)
    profile_configuration = profile_to_apply.get_configuration_for_tsn_profile()
    profile_parameters = profile_configuration.get_profile_configuration_parameters()
    for parameter, value in profile_parameters:
        profile_parameters[parameter] = (
            value + 1 if isinstance(value, int) or isinstance(value, float) else ""
        )

    netapp_identifier = tsn.NetappTrafficIdentifier(netapp_name=netapp_name)
    netapp_name_ids[netapp_name] = netapp_identifier.value()

    print(f"Generated TSN traffic identifier for Netapp: {netapp_identifier.value()}")
    print(
        f"Apply {profile_to_apply.name} with configuration parameters"
        f"{profile_configuration.get_profile_configuration_parameters()} to NetApp {netapp_name} "
    )
    clearance_token = tsn.apply_tsn_profile_to_netapp(
        profile=profile_to_apply, netapp_traffic_identifier=netapp_identifier
    )
    print(
        f"The profile configuration has been applied to the netapp. The returned token {clearance_token} can be used "
        f"to reset the configuration"
    )
    netapp_ids_tokens[netapp_identifier.value()] = clearance_token


if __name__ == "__main__":
    showcase_get_tsn_profiles()
    showcase_apply_tsn_profile_to_netapp()
    showcase_clear_profile_configuration_from_netapp()
    showcase_apply_tsn_profile_with_overriden_parameters()
