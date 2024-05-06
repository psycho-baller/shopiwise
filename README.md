# Shopiwise

Your personal shopping companion designed to empower mindful purchasing decisions

You can find the video demo [here](https://youtu.be/ZbUH-XVogsg)

## Inspiration

- Our intentions and motivations can often be complex and subconscious, leading us to make purchases that might not align with our best interests or long-term goals. Sometimes, we make purchases based on emotions, societal pressures, or habits without fully considering the consequences. Recognizing and understanding these unrecognized intentions can help us make more informed and mindful purchasing decisions
- Online shopping has become a part of our daily lives, and it's easy to get carried away with the convenience of it all. We wanted to create a tool that would help users make more mindful purchasing decisions, in the hopes of creating a world where we consume less and consume better.

## What it does

- In a world filled with tempting offers and unconscious motivations, ShopiWise provides invaluable insights into the intentions driving your shopping choices, empowering you to make more mindful purchasing decisions. By analyzing your shopping habits and providing personalized recommendations, ShopiWise helps you align your purchases with your values and long-term goals. ShopiWise is your personal shopping companion, designed to help you make more informed and mindful purchasing decisions.
- ShopiWise is a browser extension that uses a language model to analyze your shopping habits and provide personalized recommendations. It uses a vector database of knowledge on financial literacy & management, and the psychology of consumer behavior to provide insights into your shopping habits and unconscious motivations

## How we built it

- We built ShopiWise using a variety of technologies.
- For the backend:
  - Go
  - OpenAI API
- For the browser extension:
  - [Plasmo](https://docs.plasmo.com/): A framework for building Chrome extensions.
  - [Svelte](https://svelte.dev/): A JavaScript framework for building user interfaces.
  - [Tailwind CSS](https://tailwindcss.com/): A utility-first CSS framework.
  - [TypeScript](https://www.typescriptlang.org/): A typed superset of JavaScript that compiles to plain JavaScript.

## Challenges we ran into

- Who woulda thought setting up a local database postgres and redis database with docker and docker compose for the first time in a hackathon was going to be a good idea...
- Prompting the LLM, especially when I was trying to get it to always respond in JSON format

## Accomplishments that we're proud of & What we learned

- Getting the LLM to work with a vector database of knowledge on finantial literacy & management
- Finally understanding how Docker works

## What we learned

- How to manage my time better by prioritizing tasks based on how much will it positively impact the end user
- How to use Docker and Docker Compose to set up a local postgres and redis database

## What's next for Shopiwise

- Even better LLM
- Other platforms
- Even More personalized. Could be your own personal financial advisor. It can access your personal financial data, or your journal so that the LLM can give you even more personalized advice. But with that comes the responsibility of keeping your data safe and secure... from OpenAI and from us.
