# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 00:32:49 2023

@author: devik
"""


import psutil
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import Label
from tkinter import scrolledtext
from datetime import datetime
import time  # Add this line for the time.sleep function
import platform
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

MAX_DATA_POINTS = 10

# Function to gather CPU times data
def get_cpu_times():
    cpu_times = psutil.cpu_times()
    return {
        'user': cpu_times.user,
        'system': cpu_times.system,
        'idle': cpu_times.idle,
        'nice': cpu_times.nice,
    }

# Function to display CPU times pie chart
def show_cpu_times():
    cpu_times_data = get_cpu_times()

    labels = ['User', 'System', 'Idle', 'Nice']
    sizes = [
        cpu_times_data['user'],
        cpu_times_data['system'],
        cpu_times_data['idle'],
        cpu_times_data['nice'],

    ]
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']

    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('CPU Times')
    plt.show()

# Function to gather memory usage data
def get_swapped_usage():
    mem = psutil.swap_memory()
    print("mem.total, mem.used, mem.free", mem.total, mem.used, mem.free)
    return {
        'total': mem.total,
        'used': mem.percent,
        'free': 100 - mem.percent,
        'percentage': mem.percent,
        'sin': mem.sin,
        'sout': mem.sout
    }

def  get_vm_usage():
    mem = psutil.virtual_memory()
    return {
        'total': mem.total,
        'used': mem.total - mem.available,
        'percent': mem.percent,
        'free': mem.available,
    }


# Function to plot historical memory usage
def plot_historical_memory():
    historical_data = []
    timestamps = []

    for _ in range(10):  # Collect data for 10 seconds (adjust as needed)
        memory_data = get_vm_usage()
        historical_data.append(memory_data['percent'])
        timestamps.append(datetime.now().strftime('%H:%M:%S'))
        time.sleep(1)

    plt.plot(timestamps, historical_data, marker='o')
    plt.xlabel('Time')
    plt.ylabel('Memory Usage (%)')
    plt.title('Historical Memory Usage')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def show_memory_usage():
    memory_data = get_vm_usage()

    labels = 'Used', 'Free'
    sizes = [memory_data['used'], memory_data['free']]
    colors = ['#ff9999', '#66b3ff']

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    plt.title('System Memory Usage')
    plt.show()

def show_swappedMemory_usage():
    memory_data = get_swapped_usage()

    labels = 'Used', 'Free'
    sizes = [memory_data['used'], memory_data['free']]
    colors = ['#ff9999', '#66b3ff']

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    plt.title('System Swapped Memory Usage')
    plt.show()


# Function to gather network information
def get_network_info():
    network_info = psutil.net_io_counters()
    return {
        'bytes_sent': network_info.bytes_sent,
        'bytes_recv': network_info.bytes_recv,
        'packets_sent': network_info.packets_sent,
        'packets_recv': network_info.packets_recv,
    }

# Function to display network information
def show_network_info():
    network_data = get_network_info()

    labels = ['Bytes Sent', 'Bytes Received', 'Packets Sent', 'Packets Received']
    sizes = [network_data['bytes_sent'], network_data['bytes_recv'],
             network_data['packets_sent'], network_data['packets_recv']]
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']

    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Network Information')
    plt.show()

# Function to gather process information
def get_process_info():
    processes = []
    for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            mem_info = process.memory_info()
            memory_info = mem_info.rss / (1024 ** 2)  # Convert to MB
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            memory_info = 0  # Handle exceptions as needed
        processes.append({
            'pid': process.info['pid'],
            'name': process.info['name'],
            'cpu_percent': process.info['cpu_percent'],
            'memory_info': memory_info  # Convert to MB
        })
    return processes

def update_memory_plot(fig, ax, root):
    memory_data = get_vm_usage()
    historical_data.append(memory_data['percent'])
    timestamps.append(datetime.now().strftime('%H:%M:%S'))

    ax.clear()  # Clear the previous plot to update with new data
    ax.plot(timestamps, historical_data, marker='o')  # Update the plot
    # if len(historical_data) > MAX_DATA_POINTS:
    #     historical_data.pop(0)
    #     timestamps.pop(0)

    num_points = len(timestamps)
    if num_points > MAX_DATA_POINTS:
        step = num_points // MAX_DATA_POINTS
        ax.set_xticks(timestamps[::step])
    else:
        ax.set_xticks(timestamps)

    ax.set_xlabel('Time')
    ax.set_ylabel('Memory Usage (%)')
    ax.set_title('Historical Memory Usage')
    ax.set_ylim(50, 100)  # Set the y-axis limits to 0 and 100%

    
    ax.relim()  # Recalculate limits
    ax.autoscale_view()  # Autoscale
    fig.canvas.draw()  # Update the plot

    # Schedule the next update after 1 second (1000 milliseconds)
    root.after(1000, update_memory_plot, fig, ax, root)

def plot_historical_memory_New(root):
    global historical_data, timestamps
    
    historical_data = []
    timestamps = []

    fig, ax = plt.subplots()
    update_memory_plot(fig, ax, root)

    plt.xlabel('Time')
    plt.ylabel('Memory Usage (%)')
    plt.title('Historical Memory Usage')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# Function to display process information
def show_process_info():
    process_data = get_process_info()


    # for process in process_data:

    #     print(f"PID: {process['pid']}, Name: {process['name']}, "
    #           f"CPU Percent: {process['cpu_percent']:.2f}%, Memory Usage: {process['memory_info']():.2f} MB")

# Function to plot real-time CPU and memory usage
def plot_real_time_usage():
    fig, ax1 = plt.subplots(1, 1, sharex=True)
    fig.suptitle('Real-Time CPU and Memory Usage')

    cpu_data = []
    memory_data = []
    timestamps = []

    for _ in range(60):  # Update every second for a minute (adjust as needed)
        cpu_percent = psutil.cpu_percent(interval=1)
        virtual_memory = psutil.virtual_memory()

        cpu_data.append(cpu_percent)
        memory_data.append(virtual_memory.percent)
        timestamps.append(datetime.now().strftime('%H:%M:%S'))

        ax1.plot(timestamps, cpu_data, marker='o', color='b')
        # ax2.plot(timestamps, memory_data, marker='o', color='r', label='Memory Usage')

        plt.xlabel('Time')
        ax1.set_ylabel('CPU Usage (%)')
        # ax2.set_ylabel('Memory Usage (%)')

        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.legend()
        plt.pause(1)

    plt.show()

lastBytesReceived = 0
lastBytesSent = 0

def get_network_bandwidth():
    net_io = psutil.net_io_counters()
    return net_io.bytes_recv, net_io.bytes_sent

def update_network_plot_diff(fig, ax, root):
    global lastBytesReceived, lastBytesSent
    received, sent = get_network_bandwidth()

    receivedNew = received - lastBytesReceived 
    sentNew = sent - lastBytesSent 

    lastBytesReceived = received
    lastBytesSent = sent
    memory_data = get_vm_usage()
    historical_data.append(memory_data['percent'])
    timestamps.append(datetime.now().strftime('%H:%M:%S'))

    ax.clear()  # Clear the previous plot to update with new data
    ax.plot(timestamps, historical_data, marker='o')  # Update the plot

    num_points = len(timestamps)
    if num_points > MAX_DATA_POINTS:
        step = num_points // MAX_DATA_POINTS
        ax.set_xticks(timestamps[::step])
    else:
        ax.set_xticks(timestamps)

    ax.set_xlabel('Time')
    ax.set_ylabel('Memory Usage (%)')
    ax.set_title('Historical Memory Usage')
    ax.set_ylim(50, 100)  # Set the y-axis limits to 0 and 100%

    
    ax.relim()  # Recalculate limits
    ax.autoscale_view()  # Autoscale
    fig.canvas.draw()  # Update the plot

    # Schedule the next update after 1 second (1000 milliseconds)
    root.after(1000, update_network_plot, fig, ax, root)

def update_network_plot(root, fig, ax_recv, ax_sent, canvas, label, timestamps, received_data, sent_data):
    global lastBytesReceived, lastBytesSent
    received, sent = get_network_bandwidth()

    receivedNew = received - lastBytesReceived 
    sentNew = sent - lastBytesSent 

    lastBytesReceived = received
    lastBytesSent = sent
    
    current_time = datetime.now().strftime('%H:%M:%S')

    timestamps.append(current_time)
    received_data.append(receivedNew)
    sent_data.append(sentNew)

    # print("received, sent",received, sent)
    # Clear the previous plots
    ax_recv.clear()
    ax_sent.clear()

    # Update the receive plot
    ax_recv.plot(timestamps, received_data, label='Received', marker='o', color='blue')
    ax_recv.set_xlabel('Time')
    ax_recv.set_ylabel('Received Data (bytes)')
    ax_recv.set_title(f'Received Data at {current_time}')

    # Update the send plot
    ax_sent.plot(timestamps, sent_data, label='Sent', marker='o', color='green')
    ax_sent.set_xlabel('Time')
    ax_sent.set_ylabel('Sent Data (bytes)')
    ax_sent.set_title(f'Sent Data at {current_time}')

    # Set legend for receive plot
    ax_recv.legend()

    # Set legend for send plot
    ax_sent.legend()

    # Update the canvas
    canvas.draw()

    # Update the label
    label.config(text=f'Last Update: {current_time}')

    # Schedule the next update after 1000 milliseconds (1 second)
    root.after(1000, update_network_plot, root, fig, ax_recv, ax_sent, canvas, label, timestamps, received_data, sent_data)


def plot_network_bandwidth(root):
    global lastBytesReceived, lastBytesSent
    lastBytesReceived, lastBytesSent = get_network_bandwidth()
    fig, (ax_recv, ax_sent) = plt.subplots(nrows=2, sharex=True)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

    label = Label(root, text='')
    label.pack()

    timestamps = []
    received_data = []
    sent_data = []

    # Initial plot update
    update_network_plot(root, fig, ax_recv, ax_sent, canvas, label, timestamps, received_data, sent_data)



def get_dummy_disk_usage():
    # Simulate va
    # rying disk usage for testing
    return random.uniform(20, 80)  # Generates random values between 20 and 80

def update_disk_plot(fig, ax, canvas, root, historical_data, timestamps):
    disk_percent = get_dummy_disk_usage()
    historical_data.append(disk_percent)
    timestamps.append(time.strftime('%H:%M:%S'))

    ax.clear()
    ax.plot(timestamps, historical_data, marker='o')

    num_points = len(timestamps)
    if num_points > MAX_DATA_POINTS:
        step = num_points // MAX_DATA_POINTS
        ax.set_xticks(timestamps[::step])
    else:
        ax.set_xticks(timestamps)

    ax.set_xlabel('Time')
    ax.set_ylabel('Disk Usage (%)')
    ax.set_title('Historical Disk Usage')
    ax.set_ylim(0, 100)  # Set the y-axis limits to 0 and 100%

    ax.relim()
    ax.autoscale_view()
    canvas.draw()

    root.after(1000, update_disk_plot, fig, ax, canvas, root, historical_data, timestamps)

def plot_historical_disk_usage(root):
    global disk_historical_data, disk_timestamps
    
    disk_historical_data = []
    disk_timestamps = []

    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

    update_disk_plot(fig, ax, canvas, root, disk_historical_data, disk_timestamps)

    plt.xlabel('Time')
    plt.ylabel('Disk Usage (%)')
    plt.title('Historical Disk Usage')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Function to gather system information
def get_system_info():
    uname = platform.uname()
    boot_time = psutil.boot_time()
    if psutil.MACOS:
        os_name = 'Apple'
    elif psutil.WINDOWS:
        os_name = 'Windows'
    elif psutil.LINUX:
        os_name = 'Linux'
    else:
        os_name = 'Unknown'

    platform_info = {
        'os_name': os_name,
        'node_name': uname.node.split('.')[0],
        'system_name': uname.system,
        'release_version': uname.release,
        'architecture': platform.architecture()[0],
        'processor_type': platform.processor(),
        'uptime': datetime.now() - datetime.fromtimestamp(boot_time)
    }

    return platform_info
    


# Function to display system information on the first page of GUI
def display_system_info(root):
    platform_info = get_system_info()
    memory_data=get_vm_usage()

    info_str = "OS: {}\nNode Name: {}\nSystem: {}\nRelease: {}\nArchitecture: {}\nProcessor: {}\nUptime: {}".format(
        platform_info['os_name'],
        platform_info['node_name'],
        platform_info['system_name'],
        platform_info['release_version'],
        platform_info['architecture'],
        platform_info['processor_type'],
        platform_info['uptime']
    )

    # Add memory, disk, and CPU information to the displayed information
    memory_info_str = "\n\n=== Memory Information ===\n"
    disk_info_str = "\n=== Disk Information ===\n"
    cpu_info_str = "\n=== CPU Information ===\n"

    memory_info_str += f"Total RAM: {memory_data['total'] / (1024 ** 3):.2f} GB\n"
    memory_info_str += f"Used RAM: {memory_data['used'] / (1024 ** 3):.2f} GB\n"
    memory_info_str += f"Free RAM: {memory_data['free'] / (1024 ** 3):.2f} GB\n"

    for partition in psutil.disk_partitions():
        usage = psutil.disk_usage(partition.mountpoint)
        disk_info_str += f"Partition: {partition.device}\n"
        disk_info_str += f"  Total Space: {usage.total / (1024 ** 3):.2f} GB\n"
        disk_info_str += f"  Used Space: {usage.used / (1024 ** 3):.2f} GB\n"
        disk_info_str += f"  Free Space: {usage.free / (1024 ** 3):.2f} GB\n"
        disk_info_str += f"  Disk Usage Percentage: {usage.percent}%\n"
        disk_info_str += "-------------------------\n"

    cpu_info_str += f"Physical Cores: {psutil.cpu_count(logical=False)}\n"
    cpu_info_str += f"Logical Cores: {psutil.cpu_count(logical=True)}\n"
    cpu_info_str += f"CPU Usage: {psutil.cpu_percent(interval=1)}%\n"

    info_str += memory_info_str + disk_info_str + cpu_info_str

     # Create the GUI and display the system information on the first page
    text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
    text_widget.insert(tk.END, info_str)
    text_widget.pack(fill=tk.BOTH, expand=True)    




# Function to create GUI
def create_gui():
    def show_current_memory():
        show_memory_usage()

    def show_cpu_times_chart():
        show_cpu_times()

    root = tk.Tk()
    root.title("Memory Viewer")

    # Create a new frame for buttons
    button_frame = tk.Frame(root)
    button_frame.pack()

    display_system_info(root)

    button0 = tk.Button(button_frame, text="Show Current Memory Usage", command=show_current_memory)
    button0.grid(row=0, column=0)

    button1 = tk.Button(button_frame, text="Show swapped memory Usage", command=show_swappedMemory_usage)
    button1.grid(row=0, column=1)

    button2 = tk.Button(button_frame, text="Plot Historical Memory Usage", command=lambda: plot_historical_memory_New(root))
    button2.grid(row=0, column=2)

    button3 = tk.Button(button_frame, text="Show CPU Times", command=show_cpu_times_chart)
    button3.grid(row=0, column=3)

    button4 = tk.Button(button_frame, text="Show Network Information", command=show_network_info)
    button4.grid(row=0, column=4)

    button5 = tk.Button(button_frame, text="Show Process Information", command=show_process_info)
    button5.grid(row=1, column=1)

    button6 = tk.Button(button_frame, text="Plot Real-Time CPU  Usage", command=plot_real_time_usage)
    button6.grid(row=1, column=2)

    button7 = tk.Button(button_frame, text="Plot Real-Time Network data", command=lambda: plot_network_bandwidth(root))
    button7.grid(row=1, column=3)

    button8 = tk.Button(button_frame, text="Plot Real-Disk Usage", command=lambda: plot_historical_disk_usage(root))
    button8.grid(row=1, column=4)

    root.mainloop()


if __name__ == "__main__":
    create_gui()