**Messaging System using ZeroMQ**

**Overview:**
This messaging system leverages ZeroMQ, a high-performance asynchronous messaging library, to facilitate real-time communication between users and groups. It comprises four main components: `message_server.py`, `group.py`, `user_1.py`, and `user_2.py`. These components work together to enable users to interact with each other by joining groups, sending messages, and fetching messages within a distributed environment.

**ZeroMQ:**
ZeroMQ is a lightweight and fast messaging library that provides sockets-based communication patterns such as Request-Reply, Publish-Subscribe, and Push-Pull. It abstracts away the complexities of network communication and allows seamless integration between various components in a distributed system. In this messaging system, ZeroMQ is used to establish communication channels between the message server, group servers, and users.

**Components:**

1. **message_server.py:**
   - Serves as the central hub for group registration and management.
   - Handles registration requests from group servers and provides functionalities to retrieve the list of available groups.
   - Utilizes ZeroMQ sockets to communicate with group servers and users.

2. **group.py:**
   - Represents individual groups where users can interact and exchange messages.
   - Manages group membership, message storage, and retrieval functionalities.
   - Utilizes ZeroMQ sockets to handle user requests, send and receive messages, and communicate with the message server.

3. **user_1.py and user_2.py:**
   - Act as endpoints for user interactions with the messaging system.
   - Allow users to perform actions such as joining or leaving groups, sending messages, and fetching messages.
   - Utilize ZeroMQ sockets to connect to the message server and respective group servers.

**Functionality:**

- **Get Group List:** Users can request the list of available groups from the message server, which responds with a list of live servers along with their IP addresses.
- **Join/Leave Group:** Users can join or leave a group by sending requests to the respective group server, which manages group membership accordingly.
- **Send Message:** Users can send messages to a group by specifying the group's ID and the message content. The group server receives the message and updates its message storage.
- **Fetch Messages:** Users can fetch messages from a group by specifying the group's ID and optionally providing a timestamp. The group server retrieves relevant messages based on the timestamp and sends them to the user.

**Usage:**
1. Run `message_server.py` to start the message server.
2. Run `group.py` to start the group server(s).
3. Run `user_1.py` and `user_2.py` for user interactions.

**Note:** Ensure that each user runs on different instances or ports to prevent conflicts. ZeroMQ facilitates efficient and reliable communication between the various components of the messaging system, enabling seamless real-time interactions between users and groups.