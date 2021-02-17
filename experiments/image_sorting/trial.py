import copy
import os
import random
import sys
from pathlib import Path

from psychopy import core
from psychopy import event
from psychopy import visual

# fmt: off
sys.path.append(str(Path(__file__).parents[2]))
from utils.Experiment import Experiment
# fmt: on


# Create a subclass from Experiment
class ImageSortingTask(Experiment):
    def __init__(
        self,
        experiment_name: str,
        psychopy_version: str,
        experiment_dir: str,
        input_csv: str,
    ):
        super().__init__(
            experiment_name=experiment_name,
            experiment_dir=experiment_dir,
            psychopy_version=psychopy_version,
        )

        self.load_input_from_csv(input_filename=input_csv)

        self.responses = []
        self.clock = core.Clock()

    def randomize_images(self) -> list:
        """
        Randomize the stimuli presentation order.
        """
        rand_images = self.stimuli_data
        random.shuffle(rand_images)
        return rand_images

    def present_image(self, stimulus: dict, feedback: bool):
        """
        Present a single stimulus.
        """

        size = (600, 600)

        # Flip the image if necessary
        if stimulus["upside_down"]:
            size = (600, -600)

        image = visual.ImageStim(
            win=self.win,
            image=stimulus["path"],
            units="pix",
            size=size,
        )
        image.draw()
        self.win.flip()
        self.clock.reset()
        result, rt = self.register_response(stimulus)

        # Show feedback if necessary
        if feedback:
            message = visual.TextStim(
                self.win,
                text=f"{result.capitalize()}.\nReaction Time: {rt:.3f}",
            )
            message.draw()
        self.win.flip()
        core.wait(0.3)

    def register_response(self, stimulus: dict) -> (str, float):
        """
        Register and evaluate the response of the participant to the presented stimulus.
        """
        response = event.waitKeys(keyList=["left", "right"])[0]
        if response == stimulus["correct_key"]:
            result = "correct"
        else:
            result = "incorrect"
        rt = self.clock.getTime()
        self.responses.append(
            [
                stimulus["name"],
                result,
                rt,
                stimulus["condition"],
                stimulus["content"],
                stimulus["upside_down"],
                stimulus["pres_time"],
            ]
        )

        return result, rt


class Condition:
    """
    A condition of the experiment.
    """

    def __init__(
        self,
        trial: ImageSortingTask,
        instructions: str,
        repeat_images: bool,
        upside_down: bool,
        feedback: bool,
        cond: int,
    ):
        self.trial = trial
        self.repeat_images = repeat_images
        self.upside_down = upside_down
        self.feedback = feedback
        self.instructions = instructions
        self.cond = cond
        self.images_list = self.create_images_list()

    def create_images_list(self) -> list:
        """
        Create images_list that contains information about the stimuli
        (condition, upside_down, repetition_time).
        """

        path_base = os.path.join(self.trial.experiment_dir, "input", "images")

        images_list = [
            {
                "name": os.path.splitext(image[0])[0],
                "path": os.path.join(path_base, image[0]),
                "pres_time": 1,
                "upside_down": False,
                "condition": self.cond,
                "content": image[1],
            }
            for image in self.trial.randomize_images()
        ]

        # Repeat images if necessary
        if self.repeat_images:
            images_list = self.add_repeated_images(images_list)

        # Flip some images if necessary
        if self.upside_down:
            images_list = self.flip_random_images(images_list)

        # Add correct keys based on the condition
        images_list = self.add_correct_key(images_list)

        return images_list

    def add_repeated_images(self, images_list: list) -> list:
        """
        Adds repeated images to image list
        """
        repeated_images = copy.deepcopy(images_list)
        repeated_images.extend(copy.deepcopy(repeated_images))
        random.shuffle(repeated_images)
        images_already_present = set()
        new_images_list = []
        for image in repeated_images:
            if image["path"] not in images_already_present:
                images_already_present.add(image["path"])
            else:
                image["pres_time"] = 2
            new_images_list.append(image)

        return new_images_list

    def flip_random_images(
        self,
        images_list: list,
    ) -> list:
        """
        Turn random images upside down.
        """

        # Half of the images should be flipped
        count = round(len(images_list) / 2)

        for image in random.sample(images_list, k=count):
            image["upside_down"] = True

        return images_list

    def add_correct_key(self, images_list: list) -> list:
        """
        Adds correct key to every stimulus based on the condition.
        """

        for stimulus in images_list:
            # Condition 1
            if self.cond == 1:
                if stimulus["content"] == "animal":
                    stimulus["correct_key"] = "left"
                else:
                    stimulus["correct_key"] = "right"
            # Condition 2
            elif self.cond == 2:
                if stimulus["content"] == "object":
                    stimulus["correct_key"] = "left"
                else:
                    stimulus["correct_key"] = "right"
            # Condition 3
            elif self.cond == 3:
                if stimulus["content"] == "animal" and stimulus["upside_down"]:
                    stimulus["correct_key"] = "left"
                elif stimulus["content"] == "object" and stimulus["upside_down"]:
                    stimulus["correct_key"] = "right"
                elif stimulus["content"] == "animal" and not stimulus["upside_down"]:
                    stimulus["correct_key"] = "right"
                elif stimulus["content"] == "object" and not stimulus["upside_down"]:
                    stimulus["correct_key"] = "left"

        return images_list

    def play(self):
        """
        Play this condition of the trial.
        """

        # Display instructions
        trial.display_instructions(self.instructions)

        for stimulus in self.images_list:
            # Present image
            trial.present_image(stimulus, self.feedback)


# Pause until there's a keypress
trial = ImageSortingTask(
    experiment_name="Image Sorting",
    psychopy_version="2020.2.10",
    experiment_dir=os.path.dirname(os.path.abspath(__file__)),
    input_csv="stimuli-info.csv",
)

# Create first condition of the experiment
condition_1 = Condition(
    trial,
    instructions="instructions-condition-1.txt",
    cond=1,
    repeat_images=True,
    upside_down=False,
    feedback=True,
)

# Create second condition of the experiment
condition_2 = Condition(
    trial,
    cond=2,
    instructions="instructions-condition-2.txt",
    repeat_images=True,
    upside_down=False,
    feedback=True,
)

# Create third condition of the experiment
condition_3 = Condition(
    trial,
    cond=3,
    instructions="instructions-condition-3.txt",
    repeat_images=False,
    upside_down=True,
    feedback=False,
)

# Save participant info
trial.get_participant_info(
    participant_info_csv_filename="participant-info-questions.csv",
    title="Please answer the following questions!",
)

# Create window for the trial
trial.win = visual.Window(
    fullscr=True,
    allowGUI=True,
    winType="pyglet",
    color="black",
)

# Play the first condition
condition_1.play()

# Play the second condition
condition_2.play()

# Play the third condition
condition_3.play()

# Save output
trial.save_output(
    output_csv_header=[
        "stimulus_name",
        "result",
        "reaction_time",
        "condition",
        "content",
        "upside_down",
        "pres_time",
    ],
    responses=trial.responses,
    participant_name=trial.participant_info["Participant ID:"],
)

# Save participant info to the summary
trial.save_participant_info(filename="participants-summary.csv")

# Display outro
trial.display_outro(outro_filename="outro.txt")
