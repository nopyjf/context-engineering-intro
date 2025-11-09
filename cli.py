#!/usr/bin/env python3
"""
Interactive CLI with real-time streaming for Multi-Agent Research System.

This CLI provides a conversational interface to the Research Agent with:
- Real-time streaming responses
- Tool execution visibility
- Conversation history
"""

import asyncio
from typing import List
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from pydantic_ai import Agent
from agents.research_agent import research_agent
from agents.dependencies import ResearchAgentDependencies
from agents.settings import settings

console = Console()


async def stream_agent_interaction(
    user_input: str,
    conversation_history: List[str]
) -> tuple[str, str]:
    """
    Stream agent responses with real-time tool visibility.

    This function handles the streaming execution of the Research Agent,
    displaying tool calls and results in real-time as they happen.

    Args:
        user_input: User's input message
        conversation_history: Previous conversation messages

    Returns:
        Tuple of (streamed_text, final_output)
    """
    try:
        # Set up dependencies from settings
        research_deps = ResearchAgentDependencies(
            brave_api_key=settings.brave_api_key,
            gmail_credentials_path=settings.gmail_credentials_path,
            gmail_token_path=settings.gmail_token_path
        )

        # Build context with history (keep last 6 messages)
        context = "\n".join(conversation_history[-6:]) if conversation_history else ""

        prompt = f"""Previous conversation:
{context}

User: {user_input}

Respond naturally and helpfully."""

        response_text = ""

        # Use async with agent.iter() for streaming
        async with research_agent.iter(prompt, deps=research_deps) as run:

            async for node in run:

                # User prompt node - silent start
                if Agent.is_user_prompt_node(node):
                    pass  # Clean start

                # Model request node - stream text
                elif Agent.is_model_request_node(node):
                    console.print("[bold blue]Assistant:[/bold blue] ", end="")

                    # Stream events from node.stream()
                    async with node.stream(run.ctx) as request_stream:
                        async for event in request_stream:
                            event_type = type(event).__name__

                            # Check event type by name
                            if event_type == "PartDeltaEvent":
                                if hasattr(event, 'delta') and hasattr(event.delta, 'content_delta'):
                                    delta_text = event.delta.content_delta
                                    if delta_text:
                                        console.print(delta_text, end="")
                                        response_text += delta_text

                            elif event_type == "FinalResultEvent":
                                console.print()  # New line

                # Call tools node - tool execution visibility
                elif Agent.is_call_tools_node(node):
                    async with node.stream(run.ctx) as tool_stream:
                        async for event in tool_stream:
                            event_type = type(event).__name__

                            if event_type == "FunctionToolCallEvent":
                                # Extract tool name from event.part
                                tool_name = "Unknown"
                                args = None

                                if hasattr(event, 'part'):
                                    if hasattr(event.part, 'tool_name'):
                                        tool_name = event.part.tool_name
                                    if hasattr(event.part, 'args'):
                                        args = event.part.args

                                # Display tool call with rich formatting
                                console.print(f"  🔹 [cyan]Calling tool:[/cyan] [bold]{tool_name}[/bold]")

                                if args and isinstance(args, dict):
                                    arg_preview = []
                                    for key, value in list(args.items())[:3]:
                                        val_str = str(value)
                                        if len(val_str) > 50:
                                            val_str = val_str[:47] + "..."
                                        arg_preview.append(f"{key}={val_str}")
                                    console.print(f"    [dim]Args: {', '.join(arg_preview)}[/dim]")

                            elif event_type == "FunctionToolResultEvent":
                                result = str(event.tool_return) if hasattr(event, 'tool_return') else "No result"
                                if len(result) > 100:
                                    result = result[:97] + "..."
                                console.print(f"  ✅ [green]Tool result:[/green] [dim]{result}[/dim]")

                elif Agent.is_end_node(node):
                    pass  # Clean completion

        # Get final result
        final_result = run.result
        final_output = final_result.output if hasattr(final_result, 'output') else str(final_result)

        return (response_text.strip(), final_output)

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        return ("", f"Error: {e}")


async def main():
    """
    Main conversation loop.

    Provides an interactive CLI for the Research Agent with:
    - Welcome message
    - Continuous conversation loop
    - Clean exit handling
    - Error recovery
    """
    # Show welcome panel
    welcome = Panel(
        "[bold blue]🤖 Multi-Agent Research & Email Assistant[/bold blue]\n\n"
        "[green]Features:[/green]\n"
        "  • Web search via Brave Search API\n"
        "  • Research synthesis and summarization\n"
        "  • Gmail draft creation\n"
        "  • Real-time tool execution visibility\n\n"
        "[dim]Type 'exit' or 'quit' to end the session[/dim]",
        style="blue",
        padding=(1, 2)
    )
    console.print(welcome)
    console.print()

    conversation_history = []

    while True:
        try:
            # Get user input
            user_input = Prompt.ask("[bold green]You").strip()

            # Handle exit commands
            if user_input.lower() in ['exit', 'quit']:
                console.print("\n[yellow]👋 Goodbye![/yellow]")
                break

            if not user_input:
                continue

            # Add to conversation history
            conversation_history.append(f"User: {user_input}")

            # Stream agent interaction
            streamed_text, final_response = await stream_agent_interaction(
                user_input,
                conversation_history
            )

            # Handle response display
            if streamed_text:
                # Response was streamed
                console.print()
                conversation_history.append(f"Assistant: {streamed_text}")
            elif final_response and final_response.strip():
                # Response wasn't streamed, display it
                console.print(f"[bold blue]Assistant:[/bold blue] {final_response}")
                console.print()
                conversation_history.append(f"Assistant: {final_response}")
            else:
                # No response
                console.print()

        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'exit' or 'quit' to end the session[/yellow]")
            continue

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            continue


if __name__ == "__main__":
    asyncio.run(main())
