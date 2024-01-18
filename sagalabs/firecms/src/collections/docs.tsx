import {
    buildCollection,
    buildProperty
} from "firecms";

type Doc = {
    title: string;
    content: string;
    categories: string[];
    permittedRoles: string[];
    related_docs: string[];
    last_updated: Date;
    files: Resource[];
    thumbnail_image: string;

};

type Resource = {
    fileName: string;
    file: any; // Use an appropriate type for the file, such as 'File' or a custom type if needed
};


export const docsCollection = buildCollection<Doc>({
    path: "docs",
    name: "Docs",
    group: "Main",
    description: "Collection of documentation and wiki pages for SagaLabs",
    properties: {
        title: buildProperty({
            dataType: "string",
            name: "Title",
            description: "Title of the document",
            validation: {required: true}
        }),
        thumbnail_image: buildProperty({
            dataType: "string",
            name: "Thumbnail Image",
            description: "Thumbnail image for the document",
            validation: { required: true },
            storage: {
                storagePath: "docs_thumbnails", // Specify the path in your storage for thumbnails
                acceptedFiles: ["image/*"], // Accept only images
                metadata: {
                    cacheControl: "max-age=1000000", // Set cache control headers for the uploaded images
                },
                fileName: (context) => {
                    // Generate a unique file name for the thumbnail image
                    return `thumbnail_${context.entityId}_${context.file.name}`;
                }
            }
        }),
        content: buildProperty({
            dataType: "string",
            name: "Content",
            description: "Content of the document",
            validation: {required: true},
            markdown: true
        }),
        categories: buildProperty({
            dataType: "array",
            name: "Categories",
            description: "Categories for the document",
            of: {
                dataType: "string"
            }
        }),
                // Define the permittedRoles property
        permittedRoles: buildProperty({
            dataType: "array",
            name: "Permitted Roles",
            description: "Roles that are allowed to view this document",
            of: {
                dataType: "string",
                name: "Role",
                validation: {required: true},
                enumValues: [
                    {id: "BlueTeam", label: "Blue Team", color: "blueDark"},
                    {id: "RedTeam", label: "Red Team", color: "redDarker"}
                    ]
                },
                // You can customize the config as needed for your application
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

        }),
        related_docs: buildProperty({
            dataType: "array",
            name: "Related Docs",
            description: "References to related documents",
            of: {
                dataType: "reference",
                path: "docs"
            }
        }),
        last_updated: buildProperty({
            dataType: "date",
            name: "Last Updated",
            description: "The last time the document was updated",
            autoValue: "on_update",
            mode: "date_time"
        }),
        files: buildProperty({
            dataType: "array",
            name: "Uploads",
            description: "Files to be embedded into the markdown content",
            of: {
                dataType: "map",
                name: "Resource",
                properties: {
                    fileName: buildProperty({
                        dataType: "string",
                        name: "File Name",
                        description: "The name of the file",
                        validation: { required: true }
                    }),
                    file: buildProperty({
                        dataType: "string",
                        name: "File",
                        storage: {
                            storagePath: "uploads", // specify the path in your storage
                            acceptedFiles: ["image/*", "video/*", "application/pdf", "text/*", "application/*"], // adjust this to the types of files you want to accept
                            metadata: {
                                cacheControl: "max-age=1000000",
                            },
                            fileName: (context) => {
                                // This function can generate a unique file name using the document ID and original file name
                                return `${context.entityId}_${context.file.name}`;
                            }
                        },
                        validation: { required: true }
                    })
                }
            }
        }),
    },
    permissions: ({user, authController}) => ({
        edit: true,
        create: true,
        delete: true
    }),
    textSearchEnabled: true
});
