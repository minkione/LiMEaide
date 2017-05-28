import json


class Profiler(object):
    """Maintain and impliment precomiled modules and profiles."""

    def __init__(self):
        super(Profiler, self).__init__()
        self.profiles = []
        self.profiles_dir = './profiles/'
        self.manifest = 'manifest.json'

    def load_profiles(self):
        """Load dict from JSON manifest."""
        try:
            self.profiles = json.load(
                open(self.profiles_dir + self.manifest, 'r'))
        except FileNotFoundError as e:
            print(e)

    def create_profile(self, lsb_release, uname):
        """Create a new profile a save to manifest.

        Look through the output of uname and lsb_release to determine
        versions.
        """
        distro, kver, arch = '', '', ''
        kver, arch = uname[0].split()
        for info in lsb_release:
            if "Distributor" in info:
                distro = info[16:].lower()

        profile = {
            "distro": distro,
            "kver": kver,
            "arch": arch,
            "module": "lime-{0}-{1}-{2}.ko".format(distro, kver, arch),
            "profile": "vol-{0}-{1}-{2}.zip".format(distro, kver, arch)
            }
        self.profiles.append(profile)
        json.dump(self.profiles, open(self.profiles_dir + self.manifest, 'w'))

        return profile

    def interactive_chooser(self):
        """Interactive CLI mode for choosing pre-compiled modules."""
        num_profiles = len(self.profiles)
        if num_profiles > 0:
            while True:
                for i, profile in enumerate(self.profiles):
                    print(
                        "%i) %s, %s, %s\t" %
                        (i, profile['distro'], profile['kver'],
                         profile['arch']))
                profile_val = int(input(
                    "Please select a profile. " +
                    "Enter [{}] to exit: ".format(num_profiles)))
                if profile_val == num_profiles:
                    return None
                elif profile_val > 1 or profile_val < num_profiles:
                    return profile
                else:
                    print("Please select a correct value and try agin")

    def select_profile(self, distro, kver, arch):
        """Select a profile to have the client use."""
        num_profiles = len(self.profiles)
        if num_profiles > 0:
            for profile in self.profiles:
                if profile['distro'] is distro and profile['kver'] is kver and profile['arch'] is arch:
                    return profile

            return None

    def main(self):
        """Load profiles from manifest."""
        self.load_profiles()
