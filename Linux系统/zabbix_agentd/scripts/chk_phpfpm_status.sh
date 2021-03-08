#!/bin/bash
HOST='127.0.0.1'
PORT="80"
STATUS=phpfpm_status
# Functions to return phpfpm stats
function listen_queue {
        /usr/bin/curl "http://$HOST:$PORT/$STATUS" 2>/dev/null| grep -w '^listen queue:' | awk -F":" '{print $2}'        
       }    
function max_listen_queue {
        /usr/bin/curl "http://$HOST:$PORT/$STATUS" 2>/dev/null| grep -w '^max listen queue:' | awk -F":" '{print $2}'        
       }    
function listen_queue_len {
        /usr/bin/curl "http://$HOST:$PORT/$STATUS" 2>/dev/null| grep -w '^listen queue len:' | awk -F":" '{print $2}'        
       }    
function total_processes {
        /usr/bin/curl "http://$HOST:$PORT/$STATUS" 2>/dev/null| grep 'total processes' | awk -F":" '{print $2}'        
       }  
function active_processes {
        /usr/bin/curl "http://$HOST:$PORT/$STATUS" 2>/dev/null| grep -w '^active processes' | awk -F":" '{print $2}'        
       } 
function idle_processes {
        /usr/bin/curl "http://$HOST:$PORT/$STATUS" 2>/dev/null| grep 'idle processes' | awk -F":" '{print $2}'   
        }       
function max_active_processes {
        /usr/bin/curl "http://$HOST:$PORT/$STATUS" 2>/dev/null| grep -w 'max active processes' | awk -F":" '{print $2}'   
        }      
function max_children_reached {
        /usr/bin/curl "http://$HOST:$PORT/$STATUS" 2>/dev/null| grep 'max children reached' | awk -F":" '{print $2}'   
        }    
# Run the requested function
$1
