from langchain_core.prompts import PromptTemplate

template = PromptTemplate(
    template="""
Please summarize the research paper "{paper_input}" with the following specifications:

Explanation Style: {style_input}  
Explanation Length: {length_input}

1. Mathematical Details
- Include relevant mathematical equations and concepts from the paper.
- Explain them in a way that is accessible to readers with a technical background.
- Present the mathematical concepts clearly and concisely.
- Use examples and visualizations where appropriate to enhance understanding.

2. Analogies and Examples
- Provide analogies and real-world examples to illustrate the key concepts and findings of the paper.
- Use relatable examples to help readers grasp complex ideas and understand practical applications.

Additional Instructions:
- If certain details are not available, make reasonable assumptions based on the paper's content.
- Provide a comprehensive explanation that captures the essence of the research.
- Ensure the summary is well-structured, coherent, and easy to understand.
- Clearly highlight the paper’s contributions, methodologies, and implications.
""",
    input_variables=["paper_input", "style_input", "length_input"],
    validate_template=True               # is the template valid? missing variables, etc.
)



template.save("research_paper_summary_template.json")