// SPDX-License-Identifier: GPL-3.0

pragma solidity =0.6.0;

/**
 * @title Storage
 * @dev Store & retrieve value in a variable
 */
contract Storage {
    uint256 favNumber;

    struct People {
        uint256 favNumber;
        string name;
    }

    People[] public people;
    mapping(string => uint256) public nameToFavNumber;

    // /**
    //  * @dev Store value in variable
    //  * @param num value to store
    //  */
    function store(uint256 _favNumber) public returns (uint256) {
        favNumber = _favNumber;
        return _favNumber;
    }

    /**
     * @dev Return value
     * @return value of 'number'
     */
    function retrieve() public view returns (uint256) {
        return favNumber;
    }

    function addPerson(string memory _name, uint256 _favNumber) public {
        people.push(People(_favNumber, _name));
        nameToFavNumber[_name] = _favNumber;
    }
}
