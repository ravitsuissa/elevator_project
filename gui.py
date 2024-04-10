import tkinter as tk
from elevator_st import Elevator_st
from timer_service import TimerService

class Operation:
    def __init__(self):
        self.is_default_timer = True
        self.timer_queue = {}
    def display(self, current_floor):
        pass

class ElevatorGUI:
    def __init__(self, master, elevator_st):
        self.master = master
        self.elevator_st = elevator_st
        self.current_floor = 0
        self.target_floor = 0
        self.stopping = False  # Track if the elevator is currently stopping
        self.operation_callback = None
        self.closed = False
        self.master.geometry("500x300")
        self.fan_on = False
        self.floor_buttons = []
        #label to display fan status
        self.fan_status_label = tk.Label(master, text="Fan Status: OFF")
        self.fan_status_label.pack()
        #button to toggle fan status
        self.toggle_fan_button = tk.Button(master, text="Toggle Fan", command=self.toggle_fan)
        self.toggle_fan_button.pack()
        #display current floor
        self.current_floor_label = tk.Label(master, text="Current Floor: {}".format(self.elevator_st.display_floor))
        self.current_floor_label.pack()
        #display stopping status
        self.stopping_label = tk.Label(master, text="Stopping: NO")
        self.stopping_label.pack()
        #emergency button
        self.emergency_button = tk.Button(master, text="Emergency", command=self.handle_emergency)
        self.emergency_button.pack()
        # Create label to display elevator status
        self.elevator_status_label = tk.Label(master, text="Elevator Status: Active")
        self.elevator_status_label.pack()
        #buttons for each floor
        for floor in range(6):
            button = tk.Button(master, text="Floor {}".format(floor), command=lambda f=floor: self.select_floor(f))
            button.pack()
            self.floor_buttons.append(button)


    def select_floor(self, floor):
        # Call the method to raise the event for selecting the floor and pass the selected floor
        self.elevator_st.floor = floor
        self.elevator_st.raise_floor_selected()

    def handle_emergency(self):
        #emergency stop function from ST
        self.elevator_st.raise_emergency_stop()

    def on_closing(self):
        self.closed = True


    def toggle_fan(self):
        # Toggle fan status and update label
        if self.fan_on:
            self.elevator_st.raise_fan_off()  # Call state machine method to turn off fan
            self.fan_status_label.config(text="Fan Status: OFF")
            self.fan_on = False
        else:
            self.elevator_st.raise_fan_on()   # Call state machine method to turn on fan
            self.fan_status_label.config(text="Fan Status: ON")
            self.fan_on = True

    # def update_elevator_status(self):
    #     # Check if the elevator state machine is active
    #     if self.elevator_st.is_active():
    #         self.elevator_status_label.config(text="Elevator Status: Active")
    #     else:
    #         self.elevator_status_label.config(text="Elevator Status: Inactive")


def main():
    elevator_st = Elevator_st()
    elevator_st.timer_service = TimerService()
    elevator_st.operation_callback = Operation()
    root = tk.Tk()
    gui = ElevatorGUI(root, elevator_st)
    elevator_st.enter()

    # root.mainloop()
    while gui.closed is False:
        elevator_st.run_cycle()
        if elevator_st.is_state_active(elevator_st.State.main_region_elevator_system_fan_fan_off):
            gui.fan_status_label.config(text="Fan Status: OFF")
        elif elevator_st.is_state_active(elevator_st.State.main_region_elevator_system_fan_fan_on):
            gui.fan_status_label.config(text="Fan Status: ON")

        if elevator_st.is_state_active(elevator_st.State.main_region_elevator_system_moving_waiting_for_order):
            gui.elevator_status_label.config(text="Elevator Status: InActive")
        else:
            gui.elevator_status_label.config(text="Elevator Status: Active")

        if elevator_st.is_state_active(elevator_st.State.main_region_elevator_system_stop_button_emergency_stop):
            gui.emergency_button.config(text="Emergency:The elevator is stopped")
            gui.stopping_label.config(text = "Emergency: ON")
        else:
            gui.emergency_button.config(text="Emergency")
            gui.stopping_label.config(text="Emergency: OFF")

        # Check if the state machine is in the state for displaying the current floor
        if elevator_st.is_state_active(elevator_st.State.main_region_elevator_system_display_display_floor):
            gui.current_floor_label.config(text="Current Floor: {}".format(elevator_st.display_floor))

        if elevator_st.is_state_active(elevator_st.State.main_region_elevator_system_display_display_floor):
            # Update the GUI with the current floor
            gui.current_floor_label.config(text="Current Floor: {}".format(elevator_st.current_floor))

        if elevator_st.is_state_active(elevator_st.State.main_region_elevator_system_stop_button_emergency_stop):
            gui.emergency_button.config(text="Stopped on Floor: {}".format(elevator_st.current_floor))


        root.update()
    print("exit")

if __name__ == "__main__":
    main()

