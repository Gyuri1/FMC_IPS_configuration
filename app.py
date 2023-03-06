#
# IPS Rule editor
# 
# This tool was created based on this guide:
# https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application
#
#
from flask import Flask, render_template, request, url_for, flash, redirect, abort

import datetime, time


from flask import Response

def flask_logger():
    """creates logging information"""
    for i in range(100):
        current_time = datetime.datetime.now().strftime('%H:%M:%S') + "\n"
        yield current_time.encode()
        time.sleep(1)


# FMC Credential file
import fmc_config

#ips_rule_update
import ips_rule_update

# database  
import sqlite3

# sys  
import sys

# logging 
import logging


app = Flask(__name__)

app.config['SECRET_KEY'] = 'C1sco123'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('ID is required!')
        elif not content:
            flash('Network info is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

# EDIT
@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('ID is required!')

        elif not content:
            flash('Network info is required!')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

# DELETE
@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))


# Deploy
@app.route('/deploy/', methods=('GET',))
def deploy():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()

    return Response(ips_rule_update.deploy(posts, action="block"), mimetype="text/plain", content_type="text/event-stream")
     



# Reset
@app.route('/reset/', methods=('GET',))
def reset():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()

    return Response(ips_rule_update.deploy(posts, action="alert"), mimetype="text/plain", content_type="text/event-stream")
   


# Settings
@app.route('/settings/', methods=('GET','POST'))
def settings():

    if request.method == 'POST':
        fmc_config.host = request.form['fmchost'] 
        if not fmc_config.host:
            flash('FMC hosts is required!')

        fmc_config.admin = request.form['fmcadmin'] 
        if not fmc_config.admin:
            flash('FMC admin is required!') 

        fmc_config.password = request.form['fmcpassword'] 
        if not fmc_config.password:
            flash('FMC password is required!') 

        fmc_config.ips_policy = request.form['ips_policy'] 
        if not fmc_config.ips_policy:
            flash('IPS policy name is required!')  

        fmc_config.ips_rule_number = request.form['ips_rule_number'] 
        if not fmc_config.ips_rule_number:
            flash('IPS rule number is required!')

        fmc_config.ips_rulegroup = request.form['ips_rulegroup'] 
        if not fmc_config.ips_rulegroup:
            flash('IPS rule group name is required!')                   

    return render_template('settings.html', fmchost=fmc_config.host, \
    fmcadmin=fmc_config.admin, fmcpassword=fmc_config.password, \
    ips_policy=fmc_config.ips_policy, ips_rule_number= fmc_config.ips_rule_number,\
    ips_rulegroup= fmc_config.ips_rulegroup) 
