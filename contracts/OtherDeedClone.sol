// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

contract OtherDeedClone is ERC721, Ownable {
    using Counters for Counters.Counter;
    uint256 public maxSupply = 10;
    bool public publicMintOpen = false;
    bool public allowListMintOpen = false;
    mapping(address => bool) public allowList;
    Counters.Counter private _tokenIdCounter;
    string private baseURI;
    string public baseExtension = ".json";
    using Strings for uint256;

    constructor() ERC721("Otherdeedclone", "ODC") {}

    function _baseURI() internal view virtual override returns (string memory) {
        return baseURI;
    }

    function _setBaseURI(string memory baseURI_) public onlyOwner {
        baseURI = baseURI_;
    }

    function editMintWindows(bool _publicMintOpen, bool _allowListMintOpen)
        public
        onlyOwner
    {
        publicMintOpen = _publicMintOpen;
        allowListMintOpen = _allowListMintOpen;
    }

    function allowListMint() public payable {
        require(allowListMintOpen, "allowListMint closed");
        require(allowList[msg.sender] == true, "You are not in the allowList");
        require(msg.value == 0.001 ether, "Not enough funds");

        internalMint();
    }

    function publicMint() public payable {
        require(publicMintOpen, "publicMintOpen closed");
        require(msg.value == 0.01 ether, "Not enough funds");
        internalMint();
    }

    function internalMint() internal {
        require(_tokenIdCounter.current() <= maxSupply, "We sold out");
        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        _safeMint(msg.sender, tokenId);
    }

    function withdraw(address _addr) external onlyOwner {
        // get the balance of the contract
        uint256 balance = address(this).balance;
        payable(_addr).transfer(balance);
    }

    function setAllowList(address[] calldata addresses) external onlyOwner {
        for (uint256 i = 0; i < addresses.length; i++) {
            allowList[addresses[i]] = true;
        }
    }

    function tokenURI(uint256 tokenId)
        public
        view
        virtual
        override
        returns (string memory)
    {
        require(
            _exists(tokenId),
            "ERC721Metadata: URI query for nonexistent token"
        );

        string memory currentBaseURI = _baseURI();
        return
            bytes(currentBaseURI).length > 0
                ? string(
                    abi.encodePacked(
                        currentBaseURI,
                        tokenId.toString(),
                        baseExtension
                    )
                )
                : "";
    }
}
