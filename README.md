# htmlStats-to-gbq     


-----------
## Install    

* Git clone   
```bash
git clone https://github.com/kemsakurai/htmlStats-to-gbq.git
```

* Move directory
```bash
cd htmlStats-to-gbq/
```

* pip install   
```bash
pip install -r requirements.txt
```


* Edit `gbq_conf.py`
```python
CREDENTIALS_JSON = "./credentials.json"
PROJECT = "your_project"
DATASET = "your_dataset"
TABLE = "your_table"
```


* Preparing the Flask application for execution   
```bash
export FLASK_APP=cli
```

* List Job    
```console
flask job
```

```console
Usage: flask job [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  html_stats    Save html stats in the database
  save_sitemap  Save the sitemap given as an url argument in the database
  save_to_gbq   Save html statistics in the google big query

```


* DB Migtate      
By default, the data for task management is registered in the local Sqlite database.    
```console
flask db upgrade
```

```console
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> edcec73ffb2b, empty message
INFO  [alembic.runtime.migration] Running upgrade edcec73ffb2b -> 7ca9b633d8f5, empty message
```

--------------------

## Job execution    

* Register sitemap.xml for HTML parsing.     
```bash
flask job save_sitemap https://www.monotalk.xyz/sitemap.xml
```     

* Performs HTML parsing.     
```bash
flask job html_stats
```    
* Register the HTML analysis result in BiqQuery.     
```bash
flask job save_to_gbq
```

