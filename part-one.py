#!/usr/bin/env python3

import os
from time import perf_counter_ns
from random import choice
from operator import mul

def answer(input_file):
    start = perf_counter_ns()
    with open(input_file, 'r') as input_stream:
        data = input_stream.read()
        
    components = set(map(lambda x: x.strip(':'),data.replace('\n', ' ').split(' ')))

    min_cut = len(components)
    while min_cut > 3:
        connections = {
            component: [] for component in components
        }
        for row in data.split('\n'):
            component_from, *components_to = map(lambda x: x.strip(':'), row.split(' '))
            for component_to in components_to:
                connections[component_from].append(component_to)
                connections[component_to].append(component_from)

        while len(connections) > 2:
            join_left = choice(list(connections.keys()))
            join_right = choice(list(connections[join_left]))
            combined = f'{join_left}-{join_right}'
            connections[combined] = []
            for connection in connections[join_left]:
                if connection != join_right:
                    connections[combined].append(connection)
                    connections[connection].remove(join_left)
                    connections[connection].append(combined)
            for connection in connections[join_right]:
                if connection != join_left:
                    connections[combined].append(connection)
                    connections[connection].remove(join_right)
                    connections[connection].append(combined)
            connections.pop(join_left)
            connections.pop(join_right)
        min_cut = len(next(iter(connections.values())))
        answer = mul(*map(lambda x: len(x.split('-')), connections.keys()))

    end = perf_counter_ns()

    print(f'The answer is: {answer}')
    print(f'{((end-start)/1000000):.2f} milliseconds')

input_file = os.path.join(os.path.dirname(__file__), 'input')
answer(input_file)
