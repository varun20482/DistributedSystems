### Assignment README

This assignment consists of three files: `server.py`, `seller_client.py`, and `buyer_client.py`. These files facilitate communication between sellers, buyers, and the central server.

#### Steps to Use:

1. **Run the Server:**
    - Execute `server.py` to start the server.
    - The server will start listening on port `50051`.

2. **Register Sellers:**
    - Run `seller_client.py` to register sellers with the server.
    - Each time you run `seller_client.py`, it will generate a unique seller UUID.
    - Sellers do not need to provide IP addresses, as notifications are pulled from the server.

3. **Register Buyers:**
    - Execute `buyer_client.py` to register buyers with the server.
    - Like sellers, buyers do not need to provide IP addresses.

4. **Perform Actions:**
    - Sellers and buyers can perform various actions after registration, such as selling items, searching for items, buying items, adding items to wishlists, and rating items.
    - Follow the prompts provided by the client scripts to perform these actions.

5. **Notifications:**
    - Sellers and buyers can receive notifications about item updates from the server.
    - Notifications are pulled from the server, so sellers and buyers only need to know the server's IP address.

#### Note:
- Sellers and buyers can run their respective client scripts multiple times to create unique sellers/buyers each time.
- Sellers and buyers only need to know the IP address of the server to interact with it; no IP addresses need to be provided during registration.
- The server handles communication and notifications between sellers, buyers, and the marketplace.