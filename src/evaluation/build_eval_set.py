import json
import random
from src.agent.agent import CLIENT


client = CLIENT()
llm = client.get_llm()




class EVALUATION_SET:

    def QuestionAnswerPair(self, topic, tool, llm):
        messages = [{"role": "system",
                     "content": "You generate evaluation questions for a math agent."},
                    {"role": "user", 
                     "content": f"""
                                        Topic: {topic}

                                        Generate ONE simple question related to this topic.

                                        Tool category: {tool}

                                        Rules:

                                        retrieval:
                                        - Ask a simple factual or conceptual question.
                                        - The answer should be directly available from Wikipedia.
                                        - Do NOT require calculation, solving, simplification, or SymPy.
                                        - Examples:
                                        "What is a vector space?"
                                        "What are the main properties of matrices?"
                                        "What is the definition of a derivative?"

                                        compute:
                                        - The question must require mathematical calculation, solving,
                                        simplification, or evaluation using SymPy.
                                        - Keep the mathematical problem simple and related to the topic.

                                        both:
                                        - The question must require a simple concept/formula from the topic
                                        and then a mathematical calculation using SymPy.
                                        - Both parts should be answerable using the Wikipedia topic and calculation.

                                        IMPORTANT:
                                        - Keep the question simple and clear.
                                        - Do not create complicated or multi-step questions.
                                        - Do not require information from other topics.
                                        - Do not ask questions that require advanced reasoning beyond the topic.
                                        - For retrieval questions, make sure the answer can reasonably be found
                                        directly in Wikipedia.

                                        Return ONLY valid JSON:

                                        {{"question": "..."}}"""
                        }]

        response = llm.invoke(messages)

        try:
            qa = json.loads(response.content)

            return {"question": qa["question"],"expected_tool": tool}

        except json.JSONDecodeError:
            return None


    def build_evaluation_set(self, topics, output_path, llm, no_of_samples=50):
        sample_topics = random.choices(topics, k=no_of_samples)
        
        tool_distribution = (["retrieval"] * 20 + ["compute"] * 15 + ["both"] * 15)

        random.shuffle(tool_distribution)

        evaluation_set = []

        for topic, tool in zip(sample_topics, tool_distribution):
            qa_pair = self.QuestionAnswerPair(topic=topic,
                                              tool=tool,
                                              llm=llm)

            if qa_pair:
                evaluation_set.append(qa_pair)

        with open(f"{output_path}/evaluation_set.json", "w",encoding="utf-8") as f:
            json.dump(evaluation_set, f, indent=2,ensure_ascii=False)

        print(f"Generated {len(evaluation_set)} QA pairs")

        return evaluation_set
    

