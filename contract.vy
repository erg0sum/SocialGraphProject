# Decentralized Friend Graph as a Contract
# A given contract represents a complete friendgraph.
# Multiple contract instances will contain different friendgraphs

AddFriend: event({sender: indexed(address), friend: indexed(address)})

friendList: map(address, address[256])
friendCount: map(address, int128)

@public
def addFriend(friend: address) -> bool:
    sender: address = msg.sender
    count: int128 = self.friendCount[sender]
    assert count < 256
    for i in range(256):
        if i > count:
            break
        if self.friendList[sender][i] == friend:
            return False
    self.friendList[sender][count] = friend
    self.friendCount[sender] += 1
    log.AddFriend(sender, friend)
    return True

@public
def listFriends(src: address) -> address[256]:
    return self.friendList[src]

@public
def countFriends(src: address) -> int128:
    return self.friendCount[src]
