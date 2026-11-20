from typing import Callable, Optional

from src.agents.agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain,
)


def run_research_pipeline(
    topic: str,
    progress_callback: Optional[Callable[[str, str], None]] = None,
) -> dict:
    """
    Run the four-stage research workflow.

    progress_callback(stage, message) is optional. Streamlit uses it to
    update progress while the existing pipeline is running.
    """
    if not topic or not topic.strip():
        raise ValueError("Research topic cannot be empty.")

    state = {}

    def report(stage: str, message: str) -> None:
        print(f"\n{message}")
        if progress_callback:
            progress_callback(stage, message)

    # Step 1: Search agent
    report("search", "Step 1/4: Search agent is finding relevant information...")
    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [
            ("user", f"Find recent, detailed, reliable information about the topic: {topic}")
        ]
    })
    state["search_result"] = search_result["messages"][-1].content
    print("\nSearch result:", state["search_result"])

    # Step 2: Reader agent
    report("reader", "Step 2/4: Reader agent is selecting and scraping a relevant source...")
    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"Based on these search results about '{topic}', identify the most relevant "
                f"URL and scrape it for detailed, reliable information.\n\n"
                f"Search results:\n{state['search_result'][:800]}"
            )
        ]
    })
    state["scraped_result"] = reader_result["messages"][-1].content
    print("\nScraped result:", state["scraped_result"])

    # Step 3: Writer chain
    report("writer", "Step 3/4: Writer chain is drafting the research paper...")
    research_combined = (
        f"SEARCH RESULTS:\n{state['search_result']}\n\n"
        f"DETAILED SCRAPE CONTENT:\n{state['scraped_result']}\n"
    )
    state["paper"] = writer_chain.invoke({
        "topic": topic,
        "information": research_combined,
    })
    print("\nFinal paper:", state["paper"])

    # Step 4: Critic chain
    report("critic", "Step 4/4: Critic chain is reviewing the research paper...")
    state["critique"] = critic_chain.invoke({
        "research_paper": state["paper"],
    })
    print("\nCritique:", state["critique"])

    report("complete", "All four research stages completed.")
    return state
