from PyQt5.QtWidgets import QWidget
import importlib

def load_content(frame, option_name):
    # Convert the option_name to lowercase for module import
    module_name = f'{option_name.lower()}'
    
    try:
        # Dynamically import the module
        module = importlib.import_module(module_name)
        
        # Clear the frame's layout before adding new content
        layout = frame.layout()
        if layout:
            while layout.count():
                widget = layout.takeAt(0)
                if widget.widget():
                    widget.widget().deleteLater()

        # Use the correct class name by capitalizing the first letter
        class_name = f'{option_name}Window'
        window_class = getattr(module, class_name)
        
        # Create an instance of the class and add it to the frame
        content_widget = window_class()
        frame.layout().addWidget(content_widget)
        
    except ModuleNotFoundError:
        print(f"Module '{module_name}' not found")
    except AttributeError as e:
        print(f"Error: {e}")


