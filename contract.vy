# Decentralized Friend Graph as a Contract
# A given contract represents a complete friendgraph.
# Multiple contract instances will contain different friendgraphs

AddFriend: event({sender: indexed(address), friend: indexed(address)})

friendlist: map(address, address[256])
friendCount: map(address, int128)

@public
def addFriend(friend: address):
    sender: address = msg.sender
    count: int128 = self.friendCount[sender]
    self.friendlist[friend][count] = friend
    self.friendCount[sender] += 1
    log.AddFriend(sender, friend)

@public
def getFriendList(src: address) -> address[256]:
    return self.friendlist[src]

