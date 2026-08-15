import time


class DecisionEngine:


    def __init__(self, primary, backup, mode="patience"):

        self.primary = primary
        self.backup = backup

        self.active = primary

        self.mode = mode

        self.fail_count = 0
        self.recovery_start = None


        if mode == "fast":

            self.fail_limit = 2
            self.recovery_time = 60

        else:

            self.fail_limit = 3
            self.recovery_time = 120



    def decide(self, scores):

        primary_score = scores[self.primary]
        backup_score = scores[self.backup]


        print(
            f"Primary: {primary_score}"
        )

        print(
            f"Backup: {backup_score}"
        )


        # Currently using primary
        if self.active == self.primary:


            if primary_score < 60:

                self.fail_count += 1

                print(
                    "Primary failure count:",
                    self.fail_count
                )


            else:

                self.fail_count = 0



            if (
                self.fail_count >= self.fail_limit
                and backup_score >= 70
            ):

                print(
                    "Switching to backup"
                )

                self.active = self.backup

                self.fail_count = 0



        # Currently using backup
        else:


            if primary_score >= 80:


                if self.recovery_start is None:

                    self.recovery_start = time.time()

                    print(
                        "Primary recovered, waiting..."
                    )


                elif (
                    time.time()
                    -
                    self.recovery_start
                    >= self.recovery_time
                ):

                    print(
                        "Returning to primary"
                    )

                    self.active = self.primary

                    self.recovery_start = None


            else:

                self.recovery_start = None



        return self.active
