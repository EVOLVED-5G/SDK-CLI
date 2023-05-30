import random
from evolved5g.sdk import TSNManager
import emulator_utils


#

tsn_host = "127.0.0.1"  # TSN server hostname
tsn_port = 8899  # TSN server port


netapp_ids_tokens = (
    {}
)  # Stores the clearance token of each profile application to a NetApp
netapp_name = "MyNetapp1"  # The name of our NetApp

tsn = TSNManager(  # Initialization of the TNSManager
    folder_path_for_certificates_and_capif_api_key=emulator_utils.get_folder_path_for_netapp_certificates_and_capif_api_key(),
    capif_host=emulator_utils.get_capif_host(),
    capif_https_port=emulator_utils.get_capif_https_port(),
    https=False,
    tsn_host=tsn_host,
    tsn_port=tsn_port
)



def showcase_get_tsn_profiles():
    """
    Demonstrates how to retrieve information on all the available TSN profiles
    """
    profiles = tsn.get_tsn_profiles()
    print(f"Found {len(profiles)} profiles")
    for profile in profiles:
        profile_configuration = profile.get_configuration_for_tsn_profile()

        print(
            f"Profile {profile.name} with configuration parameters { profile_configuration.get_profile_configuration_parameters()}"
        )


def showcase_apply_tsn_profile_to_netapp():
    """
    Demonstrates how to apply a TSN profile configuration to a NetApp
    """
    profiles = tsn.get_tsn_profiles()
    # For demonstration purposes,  let's select the last profile to apply,
    profile_to_apply = profiles[-1]
    profile_configuration = profile_to_apply.get_configuration_for_tsn_profile()
    # Let's create an TSN identifier for this Net App.
    # This tsn_netapp_identifier can be used in two scenarios
    # a) When you want to apply a profile configuration for your net app
    # b) When you want to clear a profile configuration for your net app
    tsn_netapp_identifier = tsn.TSNNetappIdentifier(netapp_name=netapp_name)


    print(
        f"Generated TSN traffic identifier for Netapp: {tsn_netapp_identifier.value}"
    )
    print(
        f"Apply {profile_to_apply.name} with configuration parameters"
        f"{profile_configuration.get_profile_configuration_parameters()} to NetApp {netapp_name} "
    )
    clearance_token = tsn.apply_tsn_profile_to_netapp(
        profile=profile_to_apply, tsn_netapp_identifier=tsn_netapp_identifier
    )
    print(
        f"The profile configuration has been applied to the netapp. The returned token {clearance_token} can be used "
        f"to reset the configuration"
    )

    return (tsn_netapp_identifier,clearance_token)


def showcase_clear_profile_configuration_from_netapp(tsn_netapp_identifier: tsn.TSNNetappIdentifier,clearance_token:str):
    """
    Demonstrates how to clear a previously applied TSN profile configuration from a NetApp
    """
    tsn.clear_profile_for_tsn_netapp_identifier(tsn_netapp_identifier,clearance_token)
    print(f"Cleared TSN configuration from {netapp_name}")


def showcase_apply_tsn_profile_with_overriden_parameters():
    """
    Demonstrates how to override the parameters of a TSN profile and apply it to a NetApp.
    """

    profiles = tsn.get_tsn_profiles()
    # For demonstration purposes,  let's select the first profile to apply,
    profile_to_apply = profiles[-1]
    profile_configuration = profile_to_apply.get_configuration_for_tsn_profile()
    profile_parameters = profile_configuration.get_profile_configuration_parameters()

    for parameter, value in profile_parameters.items():
        # For this example we retrieve the existing profile parameters
        # if this parameter is boolean, we just reverse it (so True parameters become False, or False parameters become True)
        profile_parameters[parameter] = not value if isinstance(value, bool) else value

    tsn_netapp_identifier = tsn.TSNNetappIdentifier(netapp_name=netapp_name)


    print(
        f"Generated TSN traffic identifier for Netapp: {tsn_netapp_identifier.value}"
    )
    print(
        f"Apply {profile_to_apply.name} with configuration parameters"
        f"{profile_configuration.get_profile_configuration_parameters()} to NetApp {netapp_name} "
    )
    clearance_token = tsn.apply_tsn_profile_to_netapp(
        profile=profile_to_apply,
        tsn_netapp_identifier=tsn_netapp_identifier
    )
    print(
        f"The profile configuration has been applied to the netapp. The returned token {clearance_token} can be used "
        f"to reset the configuration\n"
    )

    return (tsn_netapp_identifier,clearance_token)


if __name__ == "__main__":
    showcase_get_tsn_profiles()
    #When we apply a profile we get back an identifier and a clearance token.
    (tsn_netapp_identifier,clearance_token) = showcase_apply_tsn_profile_to_netapp()
    # These can be used to clear the existing configuration
    showcase_clear_profile_configuration_from_netapp(tsn_netapp_identifier,clearance_token)
    showcase_apply_tsn_profile_with_overriden_parameters()
