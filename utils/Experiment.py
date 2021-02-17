import csv
import os

from psychopy import core
from psychopy import data
from psychopy import event
from psychopy import gui
from psychopy import visual


class Experiment:
    def __init__(
        self,
        *,
        experiment_name: str,
        psychopy_version: str,
        experiment_dir: str,
    ):
        self.experiment_dir = experiment_dir
        self.experiment_name = experiment_name
        self.psychopy_version = psychopy_version
        self.participant_info = {}
        self._init_data_dir()

    def _init_data_dir(self):
        """
        Create directory for the data that is generated during the experiment,
        if it doesn't exist already.
        """

        dir_path = os.path.join(self.experiment_dir, "data")
        if os.path.isdir(dir_path):
            pass
        else:
            os.mkdir(dir_path)

    def _load_instructions(self, instructions_filename: str) -> str:
        """
        Load the instructions from the specified file
        (in the working directory).
        """
        instructions_filepath = os.path.join(
            self.experiment_dir,
            "input",
            instructions_filename,
        )
        if os.path.isfile(instructions_filepath):
            with open(instructions_filepath, "r") as f:
                return f.read()
        else:
            raise Exception(f'"{instructions_filepath}" is not found.')

    def _load_participant_questions_csv(
        self,
        csv_filename: str,
    ) -> list:
        """
        Load the questions that the participant must answer before
        starting the experiment from a csv (that is located in
        the working directory).
        """
        csv_filepath = os.path.join(
            self.experiment_dir,
            "input",
            csv_filename,
        )
        if os.path.isfile(csv_filepath):
            with open(csv_filepath, newline="") as f:
                reader = csv.reader(f)
                self.participant_info_list = [line for line in reader]
                self.participant_info_csv_header = self.participant_info_list.pop(0)
        else:
            raise Exception(f'"{csv_filepath}" is not found.')

    def display_instructions(self, instructions_filename: str):
        """
        Display the instructions in a window.
        """

        instructions = self._load_instructions(instructions_filename)
        message = visual.TextStim(
            self.win,
            text=instructions,
            height=0.05,
        )
        message.draw()
        self.win.flip()
        event.waitKeys()

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

        csv_filepath = os.path.join(
            self.experiment_dir,
            "input",
            participant_info_csv_filename,
        )
        dlg = gui.Dlg(title="Participant Information")

        if hasattr(self, "failed_participant_info_field"):
            dlg.addText(
                f'Please make sure you answered this question: "{self.failed_participant_info_field}"'
            )
        else:
            dlg.addText(
                'Thank you for participating in our experiment.\n\nPlease fill the form below!\nMake sure you answered every required question (they are marked with "[*]")!'
            )
            self._load_participant_questions_csv(csv_filename=csv_filepath)

        # Add form field to the dialog
        for field in self.participant_info_list:

            field_message = field[0]

            # Get previous answer for this field if it exists
            prev_answer = self.participant_info.get(field_message, field[3])

            # Mark question if it's required
            if field[1] == "True":
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

    def load_input_from_csv(self, *, input_filename: str):
        """
        Load stimuli data from csv (in the working directory).
        """

        filepath = os.path.join(
            self.experiment_dir,
            "input",
            input_filename,
        )
        if os.path.isfile(filepath):
            with open(filepath, newline="") as f:
                reader = csv.reader(f)
                self.stimuli_data = [line for line in reader]
                self.stimuli_data_header = self.stimuli_data.pop(0)
        else:
            raise Exception(f'"{filepath}" is not found.')

    def save_participant_info(self, *, filename=str):
        """
        Save the participants info to the specified csv file.
        """

        fieldnames = self.participant_info.keys()
        filepath = os.path.join(self.experiment_dir, "data", filename)

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
        responses: list,
        participant_name: str,
    ):
        """
        Save the response of the participant to a file.
        """

        filename = f"{participant_name}_{data.getDateStr()}.csv"
        filepath = os.path.join(self.experiment_dir, "data", filename)

        with open(filepath, "w") as f:
            base = [output_csv_header]
            base.extend(responses)
            # lines = ["".join(line) for line in base]
            writer = csv.writer(f)
            writer.writerows(base)

    def display_outro(self, *, outro_filename: str):
        """Display outro."""
        outro = self._load_instructions(outro_filename)
        message = visual.TextStim(self.win, text=outro)
        message.draw()
        self.win.flip()
        event.waitKeys()

        core.quit()
