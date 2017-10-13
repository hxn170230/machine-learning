classdef DTree < handle
    %UNTITLED Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        numnodes;
        attributes;
        leaf;
        children;
        value;
    end
    
    methods
        function r = addnode(obj,index,child)
            obj.numnodes = obj.numnodes + 1;
            obj.children(index) = child;
            
            obj.leaf = false;
            r = obj;
        end
        function r = getnumnodes(obj)
            r = obj.numnodes;
        end
        function obj = DTree(attributes, value)
            [m,n] = size(attributes);
            obj.attributes = zeros(n);
            for j=1:n
                obj.attributes(j) = attributes(j);
            end
            obj.value = value;
            obj.numnodes = 0;
            obj.leaf = true;
        end
        function obj = getChild(obj, attribute)
            obj = obj.children(attribute);
        end
    end
    
end

