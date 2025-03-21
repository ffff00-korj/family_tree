import React, { useState, useEffect } from "react";
import Tree from "react-d3-tree";
import "./FamilyTree.css";

const API_URL = "http://localhost:5000/api/tree";

export default function FamilyTree() {
    const [treeData, setTreeData] = useState(null);
    const [selectedNode, setSelectedNode] = useState(null);

    useEffect(() => {
        fetch(API_URL)
            .then((response) => response.json())
            .then((data) => setTreeData(data));
    }, []);

    const transformTree = (node) => {
        return {
            name: node.name,
            attributes: {
                birthDate: node.birthDate,
                deathDate: node.deathDate,
            },
            children: node.children?.map(transformTree) || [],
            id: node.id,
        };
    };

    const addNode = (parentId, name) => {
        const findNode = (node) => {
            if (node.id === parentId) return node;
            for (let child of node.children || []) {
                const found = findNode(child);
                if (found) return found;
            }
            return null;
        };
        fetch(`${API_URL}/add`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nodeData: { name, parentId } }),
        }).then(() => fetch(API_URL).then((res) => res.json()).then(setTreeData));
    };

    const updateNode = (nodeId, name) => {
        fetch(`${API_URL}/update`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nodeData: { id: nodeId, name } }),
        }).then(() => fetch(API_URL).then((res) => res.json()).then(setTreeData));
    };

    const deleteNode = (nodeId) => {
        fetch(`${API_URL}/delete`, {
            method: "DELETE",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id: nodeId }),
        }).then(() => fetch(API_URL).then((res) => res.json()).then(setTreeData));
    };

    if (!treeData) return <p>Loading...</p>;

    const renderCustomNode = (nodeDatum) => {
        const isSelected = selectedNode === nodeDatum.id;
        const isNodeAvailable = !(nodeDatum.children && nodeDatum.children.length >= 2);

        return (
            <foreignObject width="100%" height="100%" x="-75" y="-75">
                <div
                    className={`node-card ${isSelected ? "selected" : ""}`}
                    onClick={() => setSelectedNode(isSelected ? null : nodeDatum.id)}
                >
                    <div className="node-card-header">{nodeDatum.name}</div>
                    <div className="node-card-body">
                        {(nodeDatum.attributes?.birthDate || nodeDatum.attributes?.deathDate) && (
                            <div>
                                {nodeDatum.attributes.birthDate && (
                                    <div className="birth-date">Рождение: {nodeDatum.attributes.birthDate}</div>
                                )}
                                {nodeDatum.attributes.deathDate && (
                                    <div className="death-date">Смерть: {nodeDatum.attributes.deathDate}</div>
                                )}
                            </div>
                        )}
                    </div>

                    <div className="node-card-footer">
                        <button
                            onClick={(e) => { e.stopPropagation(); addNode(nodeDatum.id, "Новый Узел"); }}
                            className={`action-btn plus ${!isNodeAvailable ? 'disabled' : ''}`}
                            disabled={!isNodeAvailable}
                        >
                            <i className="fas fa-user-plus"></i>
                        </button>

                        <button
                            onClick={(e) => { e.stopPropagation(); updateNode(nodeDatum.id, "Обновленное Имя"); }}
                            className="action-btn edit"
                        >
                            <i className="fas fa-pen"></i>
                        </button>

                        <button
                            onClick={(e) => { e.stopPropagation(); deleteNode(nodeDatum.id); }}
                            className="action-btn delete"
                        >
                            <i className="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            </foreignObject>
        );
    };

    return (
        <div className="family-tree-container">
            <Tree
                data={transformTree(treeData)}
                translate={{ x: 300, y: 200 }}
                renderCustomNodeElement={({ nodeDatum }) => renderCustomNode(nodeDatum)}
                onNodeClick={(nodeData) => setSelectedNode(nodeData.data.id)}
                orientation="vertical"
                nodeSize={{ x: 250, y: 250 }}
                separation={{ siblings: 1.5, nonSiblings: 2.5 }}
                zoom={1}
            />
        </div>
    );
}

