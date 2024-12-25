# Routeing Webapp Using AI Search


## Authors

* [Ibraheem Alyan - 1201180](https://www.ibraheemalayan.dev/)    
* Noor Al-Deen Tirhi - 1190081    

## Deployment

view the deployed version here 👉 [p1.encs3340.unv.ibraheemalayan.dev](https://p1.encs3340.unv.ibraheemalayan.dev/)

https://github.com/user-attachments/assets/42771553-abd4-4b84-b610-c59c0559e9d9

## Features

* Selectable source
* Selectable destination/s
* Multiple destinations
* 2 heuristics [aerial, walking] 
* 3 cost functions  [aerial, walking, driving] 
* 4 different algorithims [UCS, BFS, A*, Greedy] with different combinations of cost, heuristic
* Changable limit of edge length ( adjust graph density )
* Real world data for walking and driving distances scraped fromn google maps APIs
* Real coordinates for city centers, aerial distances calculated using the earth radius and coordinates
* Real map in the UI (navigatable) displaying data in real positions (nodes and edges)
* Choose source and destination on map
* Beautiful UI Design (with some animations)
* 6 different A* combinations
* 2 different Greedy Combinations
* 3 different UCS combinations
* 1 BFS comination

## Data Source

Google maps distance matrix api, see the [scrap/scraper.py](scrap/scraper.py) that was used to get the data

## Local Installation

* Install **Python** >= 3.9 (must support typing syntax)
* Install **python pip**
* Add Python, scripts to PATH
    * Windows
       ``` 
        {Python_dir}\Python39\Scripts\
        {Python_dir}\Python39\
       ```
    
    * Unix ( mac / linux )
        
        ```
        No need to add anything
        ```

* Python Venv
    * Windows
        * create an empty directory (we'll call it route_finder_home) and create a virtual enviroment in it
        ```zsh
        mkdir route_finder_home
        cd route_finder_home
        virtualenv route_finder_venv
        route_finder_venv\bin\activate
        ```
    
    * Unix ( mac / linux )

        * create an empty directory (we'll call it route_finder_home) and create a virtual enviroment in it
        
        ```
        mkdir route_finder_home
        cd route_finder_home
        python3 -m venv route_finder_venv
        source route_finder_venv/bin/activate
        ```

* Clone Repository

    ```zsh
    git clone https://github.com/ibraheemalayan/ENCS3340-AI-PathFinder-WebApp    
    ```
    ```zsh
    cd ENCS3340-AI-PathFinder-WebApp    
    ```

* Install required modules

    ```zsh
    python3 -m pip install -r requirements.txt
    ```

* Running the server

    ```zsh    
    flask run    
    ```    
    or if not in the path
    ```zsh    
    python3 -m flask run    
    ```   


* open the website [localhost:9000](http://localhost:9000/)
