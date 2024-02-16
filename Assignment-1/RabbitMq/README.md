# Youtube using RabbitMQ

## Overview:
This messaging system utilizes RabbitMQ, a message broker that implements the Advanced Message Queuing Protocol (AMQP), to enable real-time communication between users and youtubers. It consists of three main components: `YoutubeServer.py`, `User.py`, and `Youtuber.py`. These components work together to facilitate subscription management and video publication within a distributed environment.

## Components:

1. **YoutubeServer.py:**
   - Listens for subscription requests and video publication messages via RabbitMQ.
   - No direct user input required.

2. **User.py:**
   - Command-line input format:
     ```
     python User.py <UserName> [s/u <YoutuberName>]
     ```
     - `<UserName>`: The name of the user.
     - `[s/u <YoutuberName>]`: Optional. Specify either `s` to subscribe or `u` to unsubscribe to/from a youtuber, followed by the `<YoutuberName>` to perform the action on.

   - **Functionality:**
     - **Subscribe (s):** Allows a user to subscribe to a youtuber.
     - **Unsubscribe (u):** Allows a user to unsubscribe from a youtuber.

3. **Youtuber.py:**
   - Command-line input format:
     ```
     python Youtuber.py <YoutuberName> <VideoName>
     ```
     - `<YoutuberName>`: The name of the youtuber.
     - `<VideoName>`: The name of the video to be published.

   - **Functionality:**
     - **Publish Video:** Allows a youtuber to publish a video with the specified name.

## Usage:
1. Run `YoutubeServer.py` to start the server.
2. Run `User.py` to interact with the messaging system as a user.
3. Run `Youtuber.py` to publish videos as a youtuber.

Ensure RabbitMQ is installed and running before executing the components.
