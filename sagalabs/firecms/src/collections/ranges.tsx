import {
    buildCollection,
    buildProperty,
    EntityReference,
    AdditionalFieldDelegate
} from "firecms";


type AlternativeAnswer = {
    type: "string" | "regex";
    value: string;
};

type Flag = {
    description: string;
    correctValue: string;
    alternativeValues: AlternativeAnswer[];
    points: number;
};

type Resource = {
    fileName: string;
    file: any;  // Use an appropriate type for the file
};

type TTP = {
    name: string;
    link: string;
};

type Range = {
    title: string;
    thumbnail_image: string;
    story: string;
    range_name: string;
    flags: Flag[];
    ttps: TTP[];
    overview: string;
    resources: Resource[];
    difficulty: string;
    permittedRoles: string[];
};

export const rangesCollection = buildCollection<Range>({
    path: "ranges",
    name: "Ranges",
    group: "Main",
    description: "List of the ranges for SagaLabs",
    textSearchEnabled: true,
    properties: {
        title: buildProperty({
            dataType: "string",
            name: "Title",
            description: "The Title of the lab",
            validation: {required: true}
        }),
        difficulty: buildProperty({
            dataType: "string",
            name: "Difficulty",
            description: "Level of difficulty for the lab",
            validation: {required: true},
            enumValues: [
                {id: "Easy", label: "Easy", color: "greenLight"},
                {id: "Moderate", label: "Moderate", color: "blueLight"},
                {id: "Challenging", label: "Challenging", color: "yellowLight"},
                {id: "Hard", label: "Hard", color: "orangeDark"},
                {id: "Expert", label: "Expert", color: "redDark"}
            ]
        }),
        thumbnail_image: buildProperty({
            dataType: "string",
            name: "Thumbnail Image",
            storage: {
                mediaType: "image",
                storagePath: "images",
                acceptedFiles: ["image/*"],
                metadata: {
                    cacheControl: "max-age=1000000"
                }
            },
            validation: {
                required: true
            }
        }),
        story: buildProperty({
            dataType: "string",
            name: "Story",
            description: "Background story for the lab",
            validation: {required: true},
            markdown: true
        }),
        range_name: buildProperty({
            dataType: "string",
            name: "Range Name",
            validation: {required: true}
        }),
        permittedRoles: buildProperty({
            dataType: "array",
            name: "Permitted Roles",
            description: "Roles that are allowed to view this range",
            of: {
                dataType: "string",
                name: "Role",
                validation: {required: true},
                enumValues: [
                    {id: "BlueTeam", label: "Blue Team", color: "blueDark"},
                    {id: "RedTeam", label: "Red Team", color: "redDarker"}
                ],
                config: {
                    disabled: false,
                    multiple: true,
                    freeSolo: false,
                    clearOnBlur: true,
                    disableCloseOnSelect: false,
                    disableClearable: false,
                    disablePortal: false,
                    fullWidth: true,
                    selectOnFocus: false
                }
            }
        }),
        flags: buildProperty({
            dataType: "array",
            name: "Flags",
            description: "List of flags for CTF",
            of: {
                dataType: "map",
                name: "Flag",
                properties: {
                    description: buildProperty({
                        dataType: "string",
                        name: "Description",
                        validation: {required: true}
                    }),
                    correctValue: buildProperty({
                        dataType: "string",
                        name: "Correct Value",
                        validation: {required: true}
                    }),
                    alternativeValues: buildProperty({
                        dataType: "array",
                        name: "Alternative Values",
                        description: "Alternative answers that could be correct",
                        of: {
                            dataType: "map",
                            name: "Alternative Answer",
                            properties: {
                                type: buildProperty({
                                    dataType: "string",
                                    name: "Type",
                                    description: "Type of the answer (string/regex)",
                                    validation: {required: true},
                                    enumValues: {
                                        "string": "String",
                                        "regex": "Regex"
                                    }
                                }),
                                value: buildProperty({
                                    dataType: "string",
                                    name: "Value",
                                    description: "Value or regex pattern",
                                    validation: {required: true}
                                })
                            }
                        }
                    }),
                    points: buildProperty({  // Add this block for point scoring
                        dataType: "number",
                        name: "Points",
                        description: "Points awarded for capturing this flag",
                        validation: {required: true}
                    })
                }
            }
        }),
        ttps: buildProperty({
            dataType: "array",
            name: "TTPs from MITRE ATT&CK",
            description: "List of Tactics, Techniques, and Procedures from MITRE ATT&CK",
            of: {
                dataType: "map",
                name: "TTP",
                properties: {
                    name: buildProperty({
                        dataType: "string",
                        name: "Name",
                        validation: {required: true}
                    }),
                    link: buildProperty({
                        dataType: "string",
                        name: "Link",
                        description: "Link to the TTP documentation",
                        validation: {required: true}
                    })
                }
            }
        }),
        overview: buildProperty({ // Add this block
            dataType: "string",
            name: "Overview",
            description: "Overview HTML for the lab",
            validation: {required: true},
            markdown: true
        }),
        resources: buildProperty({
            dataType: "array",
            name: "Resources",
            description: "Uploaded resources for the lab",
            of: {
                dataType: "map",
                name: "Resource",
                properties: {
                    fileName: buildProperty({
                        dataType: "string",
                        name: "File Name Alias",
                        description: "The alias or original name for the uploaded file",
                        validation: {required: true}
                    }),
                    file: buildProperty({
                        dataType: "string",
                        name: "File",
                        storage: {
                            storagePath: "resources",
                            acceptedFiles: ["*/*"],
                            metadata: {
                                cacheControl: "max-age=1000000"
                            },
                            fileName: (context) => {
                                return `${context.entityId}_${context.file.name}`;
                            }
                        },
                        validation: {required: true}
                    })
                }
            }
        })
    },

    permissions: ({user, authController}) => ({
        edit: true,
        create: true,
        delete: true
    })
});
