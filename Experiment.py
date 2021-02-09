import os
import csv
from psychopy import visual, event, gui, core, data


class Experiment:
    def __init__(self, *, experiment_name: str, psychopy_version: str):
        self.init_data_dir()
        self.experiment_name = experiment_name
        self.psychopy_version = psychopy_version
        self.participant_info = {}

    def init_data_dir(self):
        """
        Create directory for the data that is generated during the experiment,
        if it doesn't exist already.
        """
        if os.path.isdir("data"):
            pass
        else:
            os.mkdir("data")

    def load_instructions(self, instructions_filename: str) -> str:
        """
        Load the instructions from the specified file
        (in the working directory).
        """
        if os.path.isfile(instructions_filename):
            with open(instructions_filename, "r") as f:
                return f.read()
        else:
            raise Exception(
                f'"{os.path.join(instructions_filename, os.path.getcwd())}" is not found.'
            )

    def display_instructions(self, instructions_filename: str):
        """
        Display the instructions in a window.
        """

        instructions = self.load_instructions(instructions_filename)
        message = visual.TextStim(self.win, text=instructions)
        message.draw()
        self.win.flip()
        event.waitKeys()

    def load_participant_questions_csv(
        self,
        csv_filename: str,
    ) -> list:
        """
        Load the questions that the participant must answer before
        starting the experiment from a csv (that is located in
        the working directory).
        """
        if os.path.isfile(csv_filename):
            with open(csv_filename, newline="") as f:
                reader = csv.reader(f)
                self.participant_info_list = [line for line in reader]
                self.participant_info_csv_header = self.participant_info_list.pop(0)
        else:
            raise Exception(f'"{os.path.join(os.getcwd(), csv_filename)}" is not found.')

    def get_participant_info(
        self,
        *,
        participant_info_csv_filename: str,
        title: str,
    ):
        """
        Get the specified pieces of information from the participant
        (before the experiment begins).
        """

        dlg = gui.Dlg(title="Participant Information")

        if hasattr(self, "failed_participant_info_field"):
            dlg.addText(
                f'Please make sure you answered this question: "{self.failed_participant_info_field}"'
            )
        else:
            dlg.addText(
                'Thank you for participating in our experiment.\n\nPlease fill the form below!\nMake sure you answered every required question (they are marked with "[*]")!'
            )
            self.load_participant_questions_csv(csv_filename=participant_info_csv_filename)

        # Add form field to the dialog
        for field in self.participant_info_list:

            field_message = field[0]

            # Get previous answer for this field if it exists
            prev_answer = self.participant_info.get(field_message, field[3])

            # Mark question if it's required
            if field[1] is True:
                field_message = f"{field_message}[*]"

            # Add fields
            if field[2] == "text_field":
                dlg.addField(field_message, prev_answer)
            elif field[2] == "single_choice":
                dlg.addField(field_message, choices=field[3].split(";"))

        answers = dlg.show()

        if not dlg.OK:
            core.quit()
        else:
            # Validate answers
            for i, answer in enumerate(answers):
                # Show dialog again if the question was required
                field_name = self.participant_info_list[i][0]
                if self.participant_info_list[i][1] == "True" and answer == "":
                    dlg.hide()
                    self.failed_participant_info_field = field_name
                    self.get_participant_info(
                        participant_info_csv_filename=participant_info_csv_filename,
                        title=title,
                    )
                    break
                else:
                    self.participant_info[field_name] = answer

        self.participant_info["date"] = data.getDateStr()
        self.participant_info["experiment_name"] = self.experiment_name
        self.participant_info["psychopyVersion"] = self.psychopy_version
        print(self.participant_info)

    def load_input_from_csv(self, *, input_filename: str):
        """
        Load stimuli data from csv (in the working directory).
        """
        if os.path.isfile(input_filename):
            with open(input_filename, newline="") as f:
                reader = csv.reader(f)
                self.stimuli_data = [line for line in reader]
                self.stimuli_data_header = self.stimuli_data.pop(0)
        else:
            raise Exception(f'"{os.path.join(os.getcwd(), input_filename)}" is not found.')

    def save_participant_info(self, *, filename=str):
        """
        Save the participants info to the specified csv file.
        """

        fieldnames = self.participant_info.keys()
        filepath = os.path.join("data", filename)

        if not os.path.isfile(filepath):
            with open(filepath, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(fieldnames)

        with open(filepath, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames)
            writer.writerow(self.participant_info)

    def save_output(
        self,
        *,
        output_csv_header: list,
        responses: list[list],
        participant_name: str,
    ):
        """
        Save the response of the participant to a file.
        """
        filename = f"{participant_name}_{data.getDateStr()}.csv"

        with open(os.path.join(os.getcwd(), "data", filename), "w") as f:
            base = [output_csv_header]
            base.extend(responses)
            # lines = ["".join(line) for line in base]
            writer = csv.writer(f)
            writer.writerows(base)

    def display_outro(self, *, outro_filename: str):
        """Display outro."""
        outro = self.load_instructions(outro_filename)
        message = visual.TextStim(self.win, text=outro)
        message.draw()
        self.win.flip()
        event.waitKeys()

        core.quit()
