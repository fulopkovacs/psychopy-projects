import os
import csv
from psychopy import visual, event, gui, core, data


class Experiment:
    def __init__(self, *, experiment_name: str, psychopy_version: str):
        self.init_data_dir()
        self.experiment_name = experiment_name
        self.psychopy_version = psychopy_version

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

    def load_participant_info_config(
        self,
        participant_info_config_filename: str,
    ) -> list:
        """
        Load the questions that the participant must answer before
        starting the experiment from a config (that is located in
        the working directory.
        """
        if os.path.isfile(participant_info_config_filename):
            with open(participant_info_config_filename, "r") as f:
                return [line.replace("\n", "") for line in f.readlines()]
        else:
            raise Exception(
                f'"{os.path.join(os.getcwd(), participant_info_config_filename)}" is not found.'
            )

    def get_participant_info(
        self,
        *,
        participant_info_config_filename: str,
        title: str,
    ):
        """
        Get the specified pieces of information from the participant
        (before the experiment begins).
        """
        participant_info_questions = self.load_participant_info_config(
            participant_info_config_filename
        )
        participant_info_dict = {}

        for question in participant_info_questions:
            participant_info_dict[question] = ""

        dlg = gui.DlgFromDict(dictionary=participant_info_dict, sortKeys=False, title=title)

        if not dlg.OK:
            core.quit()
        participant_info_dict["date"] = data.getDateStr()
        participant_info_dict["experiment_name"] = self.experiment_name
        participant_info_dict["psychopyVersion"] = self.psychopy_version
        self.participant_info = participant_info_dict

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
