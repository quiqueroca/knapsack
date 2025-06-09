# knapsack
Welcome to the knapsack challenge!
This is a fun challenge where you can submit your own solution to this version of the knapsack problem.
## The challenge
Take a look to the [items](data/knapsack_items.csv) file to see the items you can choose from.

You can select as many items as you want, but you have to respect the following constraints:
- The total weight of the items in your sack must not exceed 10 kg.
- The total volume of the items in your sack must not exceed 25 L.

The winner will be the sack with the highest value, which is calculated as the sum of the values of the items in the sack.

Note: Take into account that all the items interact with other items, modifying the value of that item if the combo item is present in the sack. 
Take into consideration that there are positive and negative combos!
<!-- leaderboard:start -->
## Leaderboard
| Name       | Weight | Volume | Value |
|------------|--------|--------|-------|
<!-- leaderboard:end -->
## How to contribute
1. Create a file under [sacks](sacks/) directory with the name of your sack like `my_super_awesome_sack.csv`. This will be your submission name.
2. Add on that file the items you want to try to pack in your sack. The file should be a CSV with an id of each item you want to submit, having 1 id per line like:
   ```csv
    1,
    2,
    3,
    ```
3. Submit a PR with your sack file. This will verify your items follow the constrains of max weight and max volume.
4. Once your PR is merged, you will be able to see your sack on the leaderboard.