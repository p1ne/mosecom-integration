#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

# Sample HTML content for testing based on actual page structure
sample_html = '''
<html>
<body>
    <h3>Последние полученные данные                    </h3>
    <div id="trl-one" class="tabs-red-line">
        <span id="pdktext" class="active">доли</span>
        <span >мг/м<sup>3</sup></span>
    </div>
    <div id="cft" class="clear-content content-for-tab">
        <div class="content-tab active">
            <div class="item-block m-flip lm4 count-green">
                <div class="m-flip__content">
                    <div class="front">
                        <div class="norma">
                            <div class="text-norma">
                                CO                                    </div>
                            <div class="info-icon"></div>
                        </div>
                        <div class="center-mode">
                            <div class="item-type">
                                <span class="first-type">
                                    Оксид углерода                                        </span>
                                <span class="total-type">
                                    <span class="this-count ">
                                        0,047                                            </span>
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="item-block m-flip lm4 count-green">
                <div class="m-flip__content">
                    <div class="front">
                        <div class="norma">
                            <div class="text-norma">
                                NO2                                    </div>
                            <div class="info-icon"></div>
                        </div>
                        <div class="center-mode">
                            <div class="item-type">
                                <span class="first-type">
                                    Диоксид азота                                        </span>
                                <span class="total-type">
                                    <span class="this-count ">
                                        0,078                                            </span>
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

# Find the "Последние полученные данные" section
current_data_pattern = r'Последние полученные данные.*?(?=<h3|<div class="dinamic")'
match = re.search(current_data_pattern, sample_html, re.DOTALL)

if match:
    print("Found current data section:")
    current_section = match.group(0)
    print(repr(current_section[:200]))  # Print first 200 chars
    
    # Find all data items
    item_pattern = r'<div class="text-norma">\s*([^<]+?)\s*</div>.*?<span class="first-type">\s*([^<]+?)\s*</span>.*?<span class="this-count ">\s*([^<]+?)\s*</span>'
    items = re.findall(item_pattern, current_section, re.DOTALL)
    
    print(f"\nFound {len(items)} items:")
    for i, item in enumerate(items):
        print(f"Item {i+1}: {item}")
else:
    print("Did not find current data section")
    
    # Let's try a more permissive pattern
    print("\nTrying more permissive pattern...")
    current_data_pattern2 = r'Последние полученные данные.*?(?=<div class="dinamic"|$)'
    match2 = re.search(current_data_pattern2, sample_html, re.DOTALL)
    
    if match2:
        print("Found current data section with permissive pattern:")
        current_section2 = match2.group(0)
        print(repr(current_section2[:200]))  # Print first 200 chars
        
        # Find all data items
        item_pattern = r'<div class="text-norma">\s*([^<]+?)\s*</div>.*?<span class="first-type">\s*([^<]+?)\s*</span>.*?<span class="this-count ">\s*([^<]+?)\s*</span>'
        items = re.findall(item_pattern, current_section2, re.DOTALL)
        
        print(f"\nFound {len(items)} items with permissive pattern:")
        for i, item in enumerate(items):
            print(f"Item {i+1}: {item}")