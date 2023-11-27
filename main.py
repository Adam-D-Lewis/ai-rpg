import os
import time

import openai
import rich


def setup():
	openai.api_key = os.getenv('OPENAI_API_KEY')
	rich.print("[bold green]OpenAI API Key set[/bold green]")
	client = openai.OpenAI()
	assistant = client.beta.assistants.create(
		name="Dungeoun Master",
		description="You are a dungeon master. You create a world, describe it to your players, and react to their actions.  Be concise.  Be creative.  Have fun!",
		model="gpt-4-1106-preview",
		tools=[
			# {"type": "code_interpreter"},{"type": "retrieval"}
			],
		file_ids=[]
	)
	thread = client.beta.threads.create()
	return client, thread, assistant
	


client, thread, assistant = setup()
while True:
	
	# add a message to the conversation thread
	message = client.beta.threads.messages.create(
		thread_id=thread.id,
		role="user",
		content=input("You: "),
	)
	
	# tell the assistant to run
	run = client.beta.threads.runs.create(
		thread_id=thread.id,
		assistant_id=assistant.id,
		# instructions="Please address the user as Jane Doe. The user has a premium account."
	)
	while run.status != "completed":
		run = client.beta.threads.runs.retrieve(
			thread_id=thread.id,
			run_id=run.id
		)
		rich.print('.', end='')
		# rich.print(f"[gray]{run.status}[/gray]")
		time.sleep(5)
	
	print()
	#retrieve and display the response
	message = client.beta.threads.messages.list(thread_id=thread.id).data[0]
	rich.print(f"[bold blue]Dungeon Master:[/bold blue] {message.content[0].text.value}")


