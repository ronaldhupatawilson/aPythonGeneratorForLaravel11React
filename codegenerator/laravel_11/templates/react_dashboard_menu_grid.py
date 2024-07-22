from codegenerator.laravel_11 import utilities

def get_dashboard_menu_grid_code(table_list):
    code = """
import React from "react";
import { Link } from "@inertiajs/react";
import {
    Grid,
    Card,
    CardActionArea,
    CardContent,
    CardMedia,
    Typography,
    CardHeader ,
    Box,
} from "@mui/material";

interface MenuItem {
    url: string;
    title: string;
    description: string;
    imagePath: string;
}

interface MenuGridProps {
    items: MenuItem[];
}

const MenuGrid = () => {
    const items = [
          
        {
            url: 'profile',
            title: 'Profile',
            description: 'change your personal details here',
            imagePath: '/images/profile.png',
        },
        {
            url: 'register',
            title: 'Register another person',
            description: 'Register someone else to have access to this website',
            imagePath: '/images/register.jpg',
        },

    """
    for table in table_list:
        code += ' '*8+'{\n'
        code += ' '*12+f"url: '{utilities.lower_case_single(table)}',\n"
        code += ' '*12+f"title: '{utilities.any_case_to_title(table)}',\n"
        code += ' '*12+f"description: 'a bit of a description about {table}',\n"
        code += ' '*12+f"imagePath: '',\n"
        code += ' '*8+'},\n'
    code += """
    ];
    return (
        <Grid container spacing={2}>
            {items.map((item, index) => (
                <Grid item xs={12} sm={6} md={4} lg={3} key={index}>
                    <Link href={item.url}>
                        <Card
                            sx={{
                                minWidth: 100,
                                minHeight: 100,
                                display: "flex",
                                flexDirection: "column",
                                height: "100%",
                                transition: "0.3s",
                                "&:hover": {
                                    transform: "scale(1.05)",
                                },
                                textDecoration: "none", // Remove default link styling
                            }}
                        >
                            <CardActionArea
                                sx={{
                                    flexGrow: 1,
                                    display: "flex",
                                    flexDirection: "column",
                                    alignItems: "stretch",
                                }}
                            >
                                {item.imagePath ? (
                                  <CardMedia
                                    component="img"
                                    height={140}
                                    image={item.imagePath || "/api/placeholder/400/320"}
                                    alt={item.title}
                                  />
                                ) : (
                                  <CardHeader
                                    title={item.title}
                                    titleTypographyProps={{ variant: "h4" }}
                                  />
                                )}
                                <CardContent
                                    sx={{
                                        flexGrow: 1,
                                        display: "flex",
                                        flexDirection: "column",
                                        justifyContent: "space-between",
                                    }}
                                >
                                    <Typography
                                        variant="body2"
                                        color="text.secondary"
                                    >
                                        {item.description || " "}
                                    </Typography>
                                </CardContent>
                            </CardActionArea>
                        </Card>
                    </Link>
                </Grid>
            ))}
        </Grid>
    );
};

export default MenuGrid;

"""
    return code
