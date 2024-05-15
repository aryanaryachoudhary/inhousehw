import os
from openai import OpenAI
from openai import AzureOpenAI


client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)






def generate_description(input):
    messages = [
        {"role": "user",
         "content": """As a Website Description Generator, Generate multi paragraph rich text website description from the information provided to you. Write
                        it in the format as described. First write the legal name of the website company, followed by the description of the company website 
                        from the information provided to you.'"""},
    ]

    # Add the scraped information to the messages
    # messages.append({"role": "user", "content": f"Product/Service: {input['product_description']}"})
    messages.append({"role": "user", "content": f"Company Name: {input['company_name']}"})
    if input['privacy_policy']:
        messages.append({"role": "user", "content": f"Privacy Policy: {input['privacy_policy']}"})
    if input['terms_of_use']:
        messages.append({"role": "user", "content": f"Terms of Use: {input['terms_of_use']}"})

    completion = client.chat.completions.create(
        model="qwe",
        messages=messages
    )
    reply = completion.choices[0].message.content.strip()
    return reply

