class Question_2_Submission:
    images_per_game = 23

    def __init__(self) -> None:
        self.image_found = True
        self.honeypot_hint = 'passed'
        self.invalid = False
        self.correct_image = None
        self.rounds = []
        self.completion_time= None
        self.correct_image_id = None
        self.hints_ids = []


    def assert_invalid_elimination_pattern(self) -> bool:
        empty_counter = 0

        # If the first 3 rounds no images were eliminated, they just wanted to achieve the minimum
        # amount of hints needed before submitting 
        for i in range(0,4):
            if self.rounds[i] == "":
                empty_counter += 1

        # If all eliminated images were selected in the 4th round they just wanted to submit asap
        if empty_counter == 3 & len(self.rounds[3]) == self.images_per_game:
            self.invalid = True

        
        return self.invalid


    def insert_honeypot_hint_id(self, honeypot_id):
        self.hints_ids[3:3] = [honeypot_id]


    def get_image_id_query(self):
        return f"""SELECT image_id FROM images WHERE path="{self.correct_image}" """


    def get_queries_hints_ids(self, hints):
        queries = []
        for hint in hints:
            queries.append(f"""SELECT hint_id FROM hints WHERE image_id={self.correct_image_id} AND hint="{hint}" """)
        
        return queries


    def get_queries_images_ids(self, round, image_paths):
        queries = []
        for image_i in round:
            queries.append(f"SELECT image_id FROM images WHERE path='{image_paths[int(image_i)]}'")
        
        return queries

        