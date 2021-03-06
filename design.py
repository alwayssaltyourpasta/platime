builder_string = """

#:import hex kivy.utils.get_color_from_hex
#:import NoTransition kivy.uix.screenmanager.NoTransition
#:import datetime datetime
#: include kv_files/today_screen.kv
#: include kv_files/task_screen.kv
#: include kv_files/statistics_screen.kv
#: include kv_files/create_task_screen.kv
#: include kv_files/add_screen.kv
#: include kv_files/workplan_screen.kv
#: include kv_files/today_progress_screen.kv
#: include kv_files/month_progress_screen.kv
#: include kv_files/year_progress_screen.kv

<ListItemWithCheckbox>:

    IconLeftWidget:
        icon: root.icon

    RightCheckbox:
        on_active: root.on_checkbox_active(*args)

#Buttons
<AddButton@MDFloatingActionButton>:
    text_color: hex('#e5e5e5')
    md_bg_color: hex('#333333')
    font_size: 100
    theme_text_color: 'Custom'
    
<NavigatorButton@MDIconButton>:
    pos_hint: {"x": 0, "y": 0}
    size_hint: (0.3, None)  

#potwierdz, cofnij
<ClassicButton@MDFlatButton>:
    text: 'zwykly przycisk'
    font_size: 10
    pos_hint: {"center_x": 0.5, "y": 0.7}
    theme_text_color: 'Custom'
    text_color: hex('#3CB371')
    md_bg_color: hex('#FFFFFF')
    
<ChooseDate@MDRectangleFlatIconButton>:
    text: "Choose date"
    icon: 'calendar'
    pos_hint: {"center_x": 0.5, "center_y": 0.55}
        
<ChooseTask@MDRectangleFlatIconButton>:
    text: "Choose task"
    icon: 'format-list-bulleted'
    pos_hint: {"center_x": 0.5, "center_y": 0.65}
<ChooseStatistics@MDRoundFlatButton>:
    size_hint: (0.3, 0.1)
    text_color: hex('#e5e5e5')
    
#Labels      
<InfoLabel@MDLabel>:
    halign: 'center'
    pos_hint: {"center_x": 0.5, "center_y": 0.86}
    theme_text_color: 'Custom'
    text_color: hex('#3CB371')
    font_style: 'Body1'
    font_size: 10
    
<Analysis@MDLabel>:
    text: "A N A L Y S I S"
    halign: 'center'
    pos_hint: {"center_x": 0.5, "center_y": 0.6}
    theme_text_color: 'Custom'
    text_color: hex('#3CB371')
    font_style: 'Body1'
    font_size: 10
<TimeProgress@MDLabel>:
    text: "T I M E"
    halign: 'center'
    pos_hint: {"center_x": 0.5, "center_y": 0.6}
    theme_text_color: 'Custom'
    text_color: hex('#3CB371')
    font_style: 'Body1'
    font_size: 10    
<Platime@MDLabel>:  
    text: 'P L A T I M E'
    halign: 'center'
    pos_hint: {"center_x":0.5, "center_y": 0.95}
    theme_text_color: 'Custom'
    text_color: hex('#e5e5e5')
    font_style: 'Overline' 
    font_size: 30  

<Date@MDLabel>:
    text: str(datetime.date.today())
    pos_hint: {"center_x":0.5, "center_y": 0.92}  
    halign: 'center'
    theme_text_color: 'Custom'
    text_color: hex('#e5e5e5')
    font_style: 'Caption' 
    font_size: 15
    
#TextFields
<EnterField@MDTextField>:
    color_mode: 'custom'
    line_color_normal: hex('#e5e5e5')
    line_color_focus: hex('#B5CBA0')
    helper_text: "It's really necessary!"
    helper_text_mode: "on_error"    
    icon_right_color: hex('#B5CBA0')
    required: True
    size_hint: (0.8, 0.1)

#ScreenManager 
Screen:
    ScreenManager:
        transition: NoTransition()
        Start:
        TodayScreen:
        TaskScreen:
        StatisticsScreen:
        TodayProgress:
        MonthProgress:
        YearProgress:
        AddTaskScreen:
        CreateTaskScreen:
        WorkPlanScreen:
        
<Start>:
    name: 'start'
       
<MyContent>:
    #height tego contentu co sie wysuwa
    adaptive_height: True
    MDIconButton:
        icon: 'check'
        size_hint: (0.25, None)
        on_release:
            root.funkcja()
        
    MDIconButton:
        icon: 'play-outline'
        size_hint: (0.25, None)
                
    MDIconButton:
        icon: 'pause-circle-outline'
        size_hint: (0.25, None)
        
    MDIconButton:
        icon: 'delete-empty-outline'
        size_hint: (0.25, None)    
         


<Content>
    size_hint_y: None
    height: self.minimum_height

    OneLineIconListItem:
        text: "Delete"
        
        IconLeftWidget:
            icon: 'delete-empty-outline'
            
    OneLineIconListItem:
        text: "Change date"
        on_release:
            root.show_datepicker()
        IconLeftWidget:
            icon: 'calendar-month-outline'      

"""