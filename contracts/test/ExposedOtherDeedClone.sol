// SPDX-License-Identifier: MIT

pragma solidity ^0.8.9;

import "../OtherDeedClone.sol";

contract ExposedOtherDeedClone is OtherDeedClone {
    using Counters for Counters.Counter;
    Counters.Counter public _tokenIdCounter;
    string public baseURI;

    constructor() {}

    function __baseURI() public view virtual returns (string memory) {
        return baseURI;
    }

    function _internalMint() public {
        require(_tokenIdCounter.current() < maxSupply, "We sold out");
        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        _safeMint(msg.sender, tokenId);
    }
}
