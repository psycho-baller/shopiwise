# Eco Enlightened

## Inspiration

Our lives are filled with habits and lifestyles that cause negative consequences without us even being aware of it, one major consequence is the impact on our environment. For that reason, we wented to create an extension for your digital life that would help you become more aware of how your actions affect the environment and how you can change them for the better.

## What it does

An extension for your digital life that makes it easy for you to learn about sustainability in the context of your life

## How we built it

The browser extension follows you everywhere and tracks what you write. It then uses Algoriths and an LLM to determine the context of what you are writing about. If the context is related to sustainability, it will show you a popup with information about the topic and personalized actions you can take to improve your impact on the environment.

## Challenges we ran into

- Who woulda thought setting up a local database postgres and redis database with docker and docker compose for the first time in a hackathon was going to be a good idea...
- Prompting the LLM to only send a response when the user is talking about sustainability. unfortunately, LLMs care about you so when you talk about how tragic your day was, it will empathize with you instead of just not responding.
- Websockets just decided to not work for us... so we just went for REST instead

## Accomplishments that we're proud of & What we learned

- Getting the LLM to work with a vector database of knowledge on sustainability
- Finally understanding how Docker works

## What's next for Eco Enlightened

- Even better LLM
- Other forms of input (voice, images, etc)
- Other topics (physical health, mental health, etc)
