def filep(x): return os.path.isfile(x)
def same(x): return x

def CONFIG(): return dict(
    why="ETHEL: multi-objective rule generator",
    which="0.1.0",
    who="Tim Menzies, MIT license (2 clause)",
    when=2018,
    how="python3 ethel.py",
    copyright="""
  """,
    what=dict(
        cohen=dict(
            why="define small changes",
            what=[
                0.2,
                0.1,
                0.3,
                0.5],
            want=float),
        DATA=dict(
            why="input data csv file",
            what='../data/auto.csv',
            make=str,
            want=filep),
        decimals=dict(
            why="decimals to display for floats",
            what=3,
            want=int),
        elite=dict(
            why="build rules from the top 'elite' number of ranges",
            what=10,
            want=int),
        few=dict(
            why="min bin size = max(few, N ^ power)",
            what=10,
            want=int), 
        least=dict(
            why="min support for acceptable rules",
            what=20,
            want=int), 
        MAIN=dict(
            why="start up action",

            what="FORMO",
            want=same),
        power=dict(
            why="min bin size = max(few, N ^ power)",
            what=0.5,
            want=float),
        speed=dict(
            why="enable heuristic domination (useful for large data sets)",
            what=False,
            want=bool),
        trivial=dict(
            why="for speed mode, min distance delta required to trigger retries",
            what=0.05,
            want=float),
        undoubt=dict(
            why="doubt reductions must be larger than x*undoubt",
            what=1.05,
            want=float),
        verbose=dict(
            why="trace all calls",
            what=False,
            want=bool),
))


  
