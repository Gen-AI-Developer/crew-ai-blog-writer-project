#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from secondflow.crews.poem_crew.blog_crew import BlogCrew


class BlogState(BaseModel):
    word_count: int = 1000
    blog: str = ""


class BlogFlow(Flow[BlogState]):

    @start()
    def generate_word_count(self):
        print("Generating word count")
        self.state.word_count = randint(950, 1000)

    @listen(generate_word_count)
    def generate_blog(self):
        print("Generating word")
        result = (
            BlogCrew()
            .crew()
            .kickoff(inputs={"word_count": self.state.word_count})
        )

        print("Blog generated", result.raw)
        self.state.blog = result.raw

    @listen(generate_blog)
    def save_poem(self):
        print("Saving Blog")
        with open("blog.txt", "w") as f:
            f.write(self.state.blog)


def kickoff():
    blog_flow = BlogFlow()
    blog_flow.kickoff()


def plot():
    blog_flow = BlogFlow()
    blog_flow.plot()


if __name__ == "__main__":
    kickoff()
