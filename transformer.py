from manim import *
import numpy as np

class VocabularyComponent:
    def __init__(self, vocab_dict, position=ORIGIN):
        self.vocab_dict = vocab_dict
        self.position = position
        self.token_mobjects = {}  # Store reference to each token's mobject
        self.vocab_group = None
        
    def animate_in(self, scene):
        """Create and return animations to show the vocabulary"""
        vocab_items = []
        
        # Create title
        vocab_title = Text("Vocabulary Dictionary", font_size=24, color=BLUE)
        vocab_title.move_to(self.position + UP * 2.3)
        
        # Create vocabulary entries
        y_offset = 1.5
        for token, token_id in self.vocab_dict.items():
            entry_text = Text(f'"{token}": {token_id}', font_size=18, color=WHITE)
            entry_text.move_to(self.position + UP * y_offset)
            
            # Store reference to this token's mobject
            self.token_mobjects[token] = entry_text
            vocab_items.append(entry_text)
            y_offset -= 0.4
        
        # Create surrounding box
        vocab_box = SurroundingRectangle(
            VGroup(*vocab_items), 
            color=BLUE, 
            buff=0.3
        )
        
        self.vocab_group = VGroup(vocab_title, vocab_box, *vocab_items)
        
        return [Write(vocab_title), Create(vocab_box), *[Write(item) for item in vocab_items]]
    
    def get_token_mobject(self, token):
        """Return the mobject representing the token in the vocabulary display"""
        return self.token_mobjects.get(token, None)
    
    def get_entry_position(self, token):
        """Return the position of the vocabulary entry for the given token"""
        entry_mobject = self.get_token_mobject(token)
        if entry_mobject:
            return entry_mobject.get_center()
        return self.position  # Fallback position




class TransformerWorkflow(Scene):
    def construct(self):
        # Title
        title = Text("Transformer Architecture: Input Processing Workflow", 
                    font_size=36, color=BLUE)
        self.play(Write(title))
        # self.play(title.animate.to_edge(UP))
        self.play(FadeOut(title))
        
        # Step 1: Input Sentence
        self.step_1_input_sentence()
        self.wait(2)
        
        # Step 2: Tokenization
        self.step_2_tokenization()
        self.wait(2)
        
        # Step 3: Input IDs
        self.step_3_input_ids()
        self.wait(2)
        
        # # Step 4: Input Embeddings
        # self.step_4_input_embeddings()
        # self.wait(3)
        
    def step_1_input_sentence(self):
        """Step 1: Show the input sentence"""
        step1_title = Text("Step 1: Input Sentence", font_size=28, color=GREEN).to_edge(LEFT + UP)
        self.play(Write(step1_title))
        
        # Input sentence
        sentence = " The cat sits on a mat "
        sentence_box = Rectangle(width=6, height=1, color=YELLOW, fill_opacity=0.2)
        sentence_text = Text(f'"{sentence}"', font_size=24, color=WHITE)
        sentence_group = VGroup(sentence_box, sentence_text).move_to(UP * 1)
        
        self.play(DrawBorderThenFill(sentence_box), Write(sentence_text))
        
        # Store for later use
        self.sentence = sentence
        self.sentence_group = sentence_group
        self.step1_title = step1_title
        
    def step_2_tokenization(self):
        """Step 2: Break sentence into individual words (tokens)"""
        step2_title = Text("Step 2: Tokenization (Word-level)", 
                          font_size=28, color=GREEN).to_edge(LEFT + UP)
        
        # Fade out step 1 title and bring in step 2
        self.play(
            Transform(self.step1_title, step2_title)
        )
        # Tokenize the sentence
        tokens = self.sentence.split()
        
        # Create individual token boxes
        token_boxes = []
        token_texts = []
        
        for i, token in enumerate(tokens):
            # Position tokens horizontally
            x_pos = (i - len(tokens)/2 + 0.5) * 2
            
            token_box = Rectangle(width=1.5, height=0.8, 
                                color=ORANGE, fill_opacity=0.3)
            token_box.move_to(RIGHT * x_pos)
            
            token_text = Text(f'{token}', font_size=20, color=WHITE)
            token_text.move_to(token_box.get_center())
            
            token_boxes.append(token_box)
            token_texts.append(token_text)
        
        # Animate the transformation from sentence to tokens
        self.play(
            self.sentence_group.animate.move_to(UP * 2.3)
            
        )
        
        # Add arrows showing the breakdown
        arrows = []
        for i, box in enumerate(token_boxes):
            arrow = Arrow(start=self.sentence_group.get_bottom() + RIGHT * (i - 1) * 0.5,
                         end=box.get_top(), color=BLUE, stroke_width=3)
            arrows.append(arrow)
        
        self.play(*[GrowArrow(arrow) for arrow in arrows],
                  *[DrawBorderThenFill(box) for box in token_boxes],
                  *[Write(text) for text in token_texts])
        
        # Store for next step
        self.tokens = tokens
        self.token_boxes = token_boxes
        self.token_texts = token_texts
        self.tokenization_group = VGroup(*token_boxes, *token_texts, self.sentence_group,arrows)
        
    def step_3_input_ids(self):
        """Step 3: Convert tokens to input IDs using vocabulary"""
        step3_title = Text("Step 3: Token to Input IDs (Vocabulary Lookup)", 
                        font_size=28, color=GREEN).to_edge(LEFT + UP)
        
        self.play(Transform(self.step1_title, step3_title))
        
        # Create a small vocabulary dictionary
        vocab_dict = {
            "The": 1,
            "cat": 5,
            "sits": 8,
            "dog": 3,
            "runs": 7,
            "sleeps": 9,
            "on": 2,
            "a": 4,
            "mat": 6
        }
        
        self.play(
            self.tokenization_group.animate.scale(0.8).move_to(LEFT * 2 + UP * 1.5),
        )
        vocab_component = VocabularyComponent(vocab_dict, position=RIGHT * 5)
        self.play(*vocab_component.animate_in(self))
        
        # Create input ID boxes (initially empty)
        input_ids = []
        id_boxes = []
        id_texts = []
        
        # Use the same scale factor as tokenization group
        scale_factor = 0.8
        
        # Pre-create all ID boxes (empty initially)
        for i, token in enumerate(self.tokens):
            x_pos = (i - len(self.tokens)/2 + 0.5) * 2 * scale_factor
            
            id_box = Rectangle(
                width=1.2 * scale_factor, 
                height=0.8 * scale_factor, 
                color=RED, 
                fill_opacity=0.3
            )
            id_box.move_to(LEFT * 2 + RIGHT * x_pos + DOWN * 1)
            
            # Create empty text initially
            id_text = Text("", font_size=int(24 * scale_factor), color=WHITE)
            id_text.move_to(id_box.get_center())
            
            id_boxes.append(id_box)
            id_texts.append(id_text)
        
        
         # Create arrows with scaled stroke width
        # Create arrows with scaled stroke width
        lookup_arrows = []  
        for i, (token_box, id_box) in enumerate(zip(self.token_boxes, id_boxes)):   
            arrow = Arrow(
            start=token_box.get_bottom() + DOWN * 0.1,  # Add small buffer
            end=id_box.get_top() + UP * 0.1, 
            color=GREEN, 
            stroke_width=3 * scale_factor,
            buff=0.1  # Minimum arrow length
        )

            lookup_arrows.append(arrow)
        # Draw all empty ID boxes
        self.play(
            *[GrowArrow(arrow) for arrow in lookup_arrows],
            *[DrawBorderThenFill(box) for box in id_boxes]
        )
        
        # Now animate each token-to-ID mapping one by one
        for i, token in enumerate(self.tokens):
            token_id = vocab_dict[token]
            input_ids.append(token_id)
            
            # 1. Highlight the current token box
            token_highlight = SurroundingRectangle(
                self.token_boxes[i], 
                color=YELLOW, 
                stroke_width=4,
                buff=0.1
            )
            self.play(Create(token_highlight))
            
            # 2. Get vocabulary entry and highlight it
            vocab_entry_mobject = vocab_component.get_token_mobject(token)
            if vocab_entry_mobject:  # Check if mobject exists
                vocab_highlight = SurroundingRectangle(
                    vocab_entry_mobject, 
                    color=ORANGE, 
                    stroke_width=3
                )
                self.play(Create(vocab_highlight))
                
                # 3. Show lookup arrow from token to vocab
                lookup_arrow = Arrow(
                    start=self.token_boxes[i].get_right(),
                    end=vocab_entry_mobject.get_left(),
                    color=GREEN, 
                    stroke_width=3 * scale_factor
                )
                self.play(GrowArrow(lookup_arrow))
                
                # 4. Show mapping arrow from vocab to ID box
                mapping_arrow = Arrow(
                    start=vocab_entry_mobject.get_bottom(),
                    end=id_boxes[i].get_top(), 
                    color=BLUE, 
                    stroke_width=3 * scale_factor
                )
                self.play(GrowArrow(mapping_arrow))
                
                # 5. Populate the ID box with the value
                new_id_text = Text(str(token_id), font_size=int(24 * scale_factor), color=WHITE)
                new_id_text.move_to(id_boxes[i].get_center())
                self.play(Transform(id_texts[i], new_id_text))
                
                # 6. Clean up highlights and arrows for this iteration
                self.play(
                    FadeOut(token_highlight),
                    FadeOut(vocab_highlight), 
                    FadeOut(lookup_arrow),
                    FadeOut(mapping_arrow)
                )
            else:
                # Fallback if vocab entry not found - just populate the ID box
                new_id_text = Text(str(token_id), font_size=int(24 * scale_factor), color=WHITE)
                new_id_text.move_to(id_boxes[i].get_center())
                self.play(
                    Transform(id_texts[i], new_id_text),
                    FadeOut(token_highlight)
                )
            
            # Brief pause between tokens
            self.wait(0.3)
        
        # Final step: Show the complete input IDs array
        ids_label_str = '[' + ', '.join(str(i) for i in input_ids) + ']'
        ids_label = Text(f"{ids_label_str}", font_size=int(30 * scale_factor), color=RED)
        ids_label.move_to(LEFT * 2 + DOWN * 3)
        
        final_arrows = []
        for i, id_box in enumerate(id_boxes):
            arrow = Arrow(
                start=id_box.get_bottom(),
                end=ids_label.get_top(), 
                color=YELLOW_B, 
                stroke_width=3 * scale_factor
            )
            final_arrows.append(arrow)
        
        # First animate the arrows
        self.play(
            *[GrowArrow(arrow) for arrow in final_arrows]
        )

        # Then display the ids_label
        self.play(
            Write(ids_label)
        )


                
        
        # Store for next step
        self.input_ids = input_ids
        self.id_boxes = id_boxes
        self.id_texts = id_texts
        self.ids_group = VGroup(*id_boxes, *id_texts)
        
    def step_4_input_embeddings(self):
        """Step 4: Convert input IDs to embeddings"""
        step4_title = Text("Step 4: Input IDs to Embeddings", 
                          font_size=28, color=GREEN).move_to(UP * 2.5)
        
        self.play(Transform(self.step1_title, step4_title))
        
        # Clear previous elements and focus on embeddings
        self.play(
            FadeOut(VGroup(*self.token_boxes, *self.token_texts)),
            self.ids_group.animate.move_to(UP * 1)
        )
        
        # Create embedding matrix representation
        embedding_dim = 4  # Small embedding dimension for visualization
        
        # Show embedding lookup table
        embed_title = Text("Embedding Matrix (vocab_size × embedding_dim)", 
                          font_size=18, color=YELLOW)
        embed_title.move_to(LEFT * 4 + UP * 1.5)
        
        # Create a simplified embedding matrix visualization
        embed_matrix = []
        for i in range(3):  # Show only relevant embeddings
            row = []
            for j in range(embedding_dim):
                # Generate some example embedding values
                value = round(np.random.normal(0, 0.5), 2)
                cell = Rectangle(width=0.8, height=0.4, color=BLUE, fill_opacity=0.2)
                cell.move_to(LEFT * 4 + LEFT * (j - 1.5) * 0.8 + DOWN * i * 0.4)
                
                text = Text(str(value), font_size=12, color=WHITE)
                text.move_to(cell.get_center())
                
                row.append(VGroup(cell, text))
            embed_matrix.append(row)
        
        # Add row labels (token IDs)
        id_labels = []
        for i, token_id in enumerate([1, 5, 8]):  # Our input IDs
            label = Text(f"ID {token_id}:", font_size=14, color=RED)
            label.move_to(LEFT * 5.5 + DOWN * i * 0.4)
            id_labels.append(label)
        
        # Animate embedding matrix
        self.play(
            Write(embed_title),
            *[Write(label) for label in id_labels],
            *[DrawBorderThenFill(cell[0]) for row in embed_matrix for cell in row],
            *[Write(cell) for row in embed_matrix for cell in row]
        )
        
        # Create final embedding vectors
        embedding_vectors = []
        vector_groups = []
        
        for i, token_id in enumerate(self.input_ids):
            x_pos = (i - len(self.input_ids)/2 + 0.5) * 2.5
            
            # Create vertical vector representation
            vector_cells = []
            for j in range(embedding_dim):
                cell = Rectangle(width=0.6, height=0.4, 
                               color=PURPLE, fill_opacity=0.4)
                cell.move_to(RIGHT * x_pos + DOWN * (2 + j * 0.4))
                
                # Generate embedding values
                value = round(np.random.normal(0, 0.5), 2)
                text = Text(str(value), font_size=10, color=WHITE)
                text.move_to(cell.get_center())
                
                vector_cells.append(VGroup(cell, text))
            
            vector_group = VGroup(*vector_cells)
            vector_groups.append(vector_group)
            
            # Add vector label
            vector_label = Text(f"E{i+1}", font_size=16, color=PURPLE)
            vector_label.move_to(RIGHT * x_pos + DOWN * 1.5)
            vector_groups[i].add(vector_label)
        
        # Animate the embedding lookup
        lookup_arrows = []
        for i, (id_box, vector_group) in enumerate(zip(self.id_boxes, vector_groups)):
            arrow = Arrow(start=id_box.get_bottom(),
                         end=vector_group[0].get_top(), color=PURPLE, stroke_width=3)
            lookup_arrows.append(arrow)
        
        self.play(
            *[GrowArrow(arrow) for arrow in lookup_arrows],
            *[DrawBorderThenFill(cell[0]) for vector in vector_groups for cell in vector[:-1]],
            *[Write(cell) for vector in vector_groups for cell in vector[:-1]],
            *[Write(vector[-1]) for vector in vector_groups]  # Labels
        )
        
        # Final summary
        summary = Text("Input Embeddings: Dense vector representations ready for transformer!",
                      font_size=18, color=GREEN)
        summary.move_to(DOWN * 3.5)
        self.play(Write(summary))
        
        # Add dimension info
        dim_info = Text(f"Shape: (sequence_length={len(self.input_ids)}, embedding_dim={embedding_dim})",
                       font_size=14, color=GRAY)
        dim_info.move_to(DOWN * 3.8)
        self.play(Write(dim_info))
        self.wait(2)